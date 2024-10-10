from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsOwner
from users.serializers import (UserPasswordResetConfirmSerializer,
                               UserPasswordResetSerializer,
                               UserRegistrationSerializer,
                               UserRetrieveSerializer)


class UserRegistrationAPIView(generics.CreateAPIView):
    """Эндпоинт создания пользователя"""
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            user.set_password(user.password)
            user.save()
            return response.Response({'detail': 'Пользователь успешно зарегистрирован'},
                                     status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=400)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт редактирования пользователя"""
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра пользователя"""
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserPasswordResetAPIView(generics.GenericAPIView):
    """Эндпоинт для сброса пароля пользователя"""
    serializer_class = UserPasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Ссылка для сброса пароля отправлена на почту."},
                                 status=status.HTTP_200_OK)


class UserPasswordResetConfirmAPIView(generics.GenericAPIView):
    """Эндпоинт для подтверждения сброса пароля пользователя"""
    serializer_class = UserPasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Пароль успешно сброшен."},
                                 status=status.HTTP_200_OK)
