import factory
import pytest
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework.test import APIClient

from callboard.models import Ad, Review
from users.models import User

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика создания пользователей"""

    class Meta:
        model = User
        skip_postgeneration_save = True

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.LazyAttribute(lambda x: fake.phone_number()[:15])
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def save_user(self, create, extracted, **kwargs):
        if create:
            self.save()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_admin():
    """Фикстура создания администратора"""
    return UserFactory.create(role=User.UsersRolesChoices.ADMIN, is_staff=True, is_superuser=True)


@pytest.fixture
def user_admin2():
    """Фикстура создания второго администратора"""
    return UserFactory.create(role=User.UsersRolesChoices.ADMIN, is_staff=True, is_superuser=True)


@pytest.fixture
def user_client():
    """Фикстура создания обычного пользователя"""
    return UserFactory.create()


@pytest.fixture
def user_client2():
    """Фикстура создания второго обычного пользователя"""
    return UserFactory.create()


@pytest.fixture
def users_list(user_client, user_client2, user_admin, user_admin2):
    """Фткстура создания списка пользователей"""
    return [user_client, user_client2, user_admin, user_admin2]


@pytest.fixture
def reset_password_data(user_client):
    """Фикстура создания данных для сброса пароля"""
    uid = urlsafe_base64_encode(force_bytes(user_client.pk))
    token = default_token_generator.make_token(user_client)
    return {
        "uid": uid,
        "token": token,
        "new_password": "new@pass@123"
    }


class AdFactory(factory.django.DjangoModelFactory):
    """Фабрика создания объявлений"""

    class Meta:
        model = Ad
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=4)
    price = factory.Faker("random_int", min=100, max=10000)
    description = factory.Faker("text")
    author = factory.SubFactory(UserFactory)


@pytest.fixture
def ad_create():
    """Фикстура создания одного объявления"""

    def _ad_create(user):
        return AdFactory.create(author=user)

    return _ad_create


@pytest.fixture
def ad_user(ad_create, user_client):
    """Фикстура создания одного объявления от юзера"""
    return ad_create(user_client)


@pytest.fixture
def ad_admin(ad_create, user_admin):
    """Фикстура создания одного объявления от админа"""
    return ad_create(user_admin)


@pytest.fixture
def ads_create():
    """Фикстура создания списка объявлений"""

    def _ads_create(user, count_ads):
        return [AdFactory.create(author=user) for _ in range(count_ads)]

    return _ads_create


@pytest.fixture
def ads_user(ads_create, user_client):
    """Фикстура создания списка объявлений от юзера"""
    return ads_create(user_client, 3)


@pytest.fixture
def ads_admin(ads_create, user_admin):
    """Фикстура создания списка объявлений от админа"""
    return ads_create(user_admin, 2)


@pytest.fixture
def ads_users(ads_user, ads_admin):
    """Фикстура создания списка объявлений от юзера и админа вместе"""
    return ads_user + ads_admin


class ReviewFactory(factory.django.DjangoModelFactory):
    """Фабрика создания комментариев"""

    class Meta:
        model = Review
        skip_postgeneration_save = True

    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
    ad = factory.SubFactory(AdFactory)


@pytest.fixture
def review_ad_create():
    """Фикстура создания одного комментария"""

    def _review_ad_create(user, ad):
        return ReviewFactory(author=user, ad=ad)

    return _review_ad_create


@pytest.fixture
def review_user_ad(review_ad_create, user_client, ad_user):
    """Фикстура создания одного комментария от юзера"""
    return review_ad_create(user_client, ad_user)


@pytest.fixture
def review_admin_ad(review_ad_create, user_admin, ad_user):
    """Фикстура создания одного комментария от админа"""
    return review_ad_create(user_admin, ad_user)


@pytest.fixture
def ad_with_reviews(review_ad_create, user_client, users_list, review_count=2):
    """Фикстура создания объявления с несколькими комментариями"""
    ad = AdFactory.create(author=user_client)
    for _ in range(review_count):
        for user in users_list:
            review_ad_create(user, ad)
    return ad
