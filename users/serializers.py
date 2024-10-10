from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Класс сериализатор пользователя"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'phone', 'email', 'role', 'image']

    def validate_role(self, value):
        if value not in ['admin', 'user']:
            raise serializers.ValidationError('Недопустимая роль!')
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.is_active = True
        if user.role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserRetrieveSerializer(serializers.ModelSerializer):
    """Класс сериализатор отображения профиля пользователя"""

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'role', 'image', 'is_active']


class UserPasswordResetSerializer(serializers.Serializer):
    """Класс сериализатор сброса пароля пользователя"""
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email не зарегистрирован.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = settings.PASSWORD_RESET_CONFIRM_URL.format(uid=uid, token=token)
        send_mail(
            'Сброс пароля',
            f'Перейдите по следующей ссылке, чтобы сбросить пароль: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    """Класс сериализатор подтверждения сброса пароля пользователя"""
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        uid = self.context.get('view').kwargs.get('uid')
        if not uid:
            uid = attrs.get('uid')
        token = self.context.get('view').kwargs.get('token')
        if not token:
            token = attrs.get('token')
        new_password = attrs.get('new_password')
        user_id = urlsafe_base64_decode(uid)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Невалидный UID.")
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Невалидный токен.")
        return attrs

    def save(self):
        uid = self.context.get('view').kwargs.get('uid')
        if not uid:
            uid = self.validated_data['uid']
        user_id = urlsafe_base64_decode(uid)
        new_password = self.validated_data['new_password']
        user = User.objects.get(pk=user_id)
        user.set_password(new_password)
        user.save()
