from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """Модель пользователя"""

    class UsersRolesChoices(models.TextChoices):
        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')

    username = None
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=35, verbose_name='Телефон')
    email = models.EmailField(unique=True, verbose_name='Почта')
    role = models.CharField(max_length=10, choices=UsersRolesChoices,
                            default=UsersRolesChoices.USER, verbose_name='Роль')
    image = models.ImageField(upload_to='users/', default='users/no_avatar.png',
                              **NULLABLE, verbose_name='Аватар')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
