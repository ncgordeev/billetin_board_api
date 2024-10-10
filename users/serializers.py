from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Класс сериализатор пользователя"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'phone', 'email', 'role', 'image']

    def create(self, data):
        user = User(**data)
        user.is_active = True
        if user.role == User.UsersRolesChoices.ADMIN:
            user.is_staff = True
            user.is_superuser = True
        user.set_password(data['password'])
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
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"detail": "Невалидный UID."})

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Невалидный токен."})
        attrs['user'] = user
        return attrs

    def save(self):
        uid = self.validated_data['uid']
        user_id = urlsafe_base64_decode(uid)
        new_password = self.validated_data['new_password']
        user = User.objects.get(pk=user_id)
        user.set_password(new_password)
        user.save()
