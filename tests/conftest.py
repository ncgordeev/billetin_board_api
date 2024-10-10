import factory
import pytest
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework.test import APIClient

from users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика создания пользователей"""

    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyAttribute(lambda x: fake.phone_number()[:15])
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_active = True
    is_staff = False
    is_superuser = False


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_admin():
    """Фикстура создания администратора"""
    return UserFactory.create(role=User.UsersRolesChoices.ADMIN, is_staff=True, is_superuser=True)


@pytest.fixture
def user_client():
    """Фикстура создания обычного пользователя"""
    return UserFactory.create()


@pytest.fixture
def user_anonymous():
    """Фикстура создания анонимного пользователя"""
    return APIClient()


@pytest.fixture
def reset_password_data(user_client):
    uid = urlsafe_base64_encode(force_bytes(user_client.pk))
    token = default_token_generator.make_token(user_client)
    return {
        "uid": uid,
        "token": token,
        "new_password": "new@pass@123"
    }
