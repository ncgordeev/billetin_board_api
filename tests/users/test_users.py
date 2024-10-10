import pytest
from django.test import RequestFactory
from django.urls import reverse

from tests.conftest import UserFactory
from users.models import User
from users.serializers import UserRetrieveSerializer


@pytest.mark.django_db
class TestUsers:
    """Тестирование приложения Users"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, user_admin, user_client):
        self.api_client = api_client
        self.user_admin = user_admin
        self.user_client = user_client
        self.factory = RequestFactory()

    @pytest.mark.parametrize("first_name, last_name, phone, email, role, password, expected_status, expected_detail", [
        ("f_name1", "l_name1", "+7(000)123-45-67", "test@example1.com", "user", "Qwe123ewQ",
         201, "Пользователь успешно зарегистрирован!"),
        ("f_name2", "l_name2", "+7(000)123-45-68", "test@example2.com", "admin", "Qwe123ewQ",
         201, "Пользователь успешно зарегистрирован!"),
        ("f_name3", "l_name3", "+7(000)123-45-69", "test@example3.com", "hacker", "Qwe123ewQ",
         400, "Недопустимая роль!"),
        ("f_name4", "l_name4", "+7(000)123-45-70", "test@example1.com", "user", "Qwe123ewQ",
         400, "Данный email уже зарегистрирован!")
    ])
    def test_user_create(self, api_client, first_name, last_name, phone, email,
                         role, password, expected_status, expected_detail):
        """
        Тестирование создания пользователя
        [POST] http://127.0.0.1:8000/users/create/
        """
        if expected_status == 400 and expected_detail == "Данный email уже зарегистрирован!":
            UserFactory.create(email=email)
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "role": role,
            "password": password
        }
        response = api_client.post(reverse('users:user_create'), data=data, format='json')

        assert response.status_code == expected_status
        if response.status_code == 201:
            assert response.data['detail'] == expected_detail
        else:
            error_messages = response.data
            if 'role' in error_messages:
                assert any("Недопустимая роль!" in str(err) or
                           f"Значения {role} нет среди допустимых вариантов." in str(err)
                           for err in error_messages['role'])
            elif 'email' in error_messages:
                assert any("Данный email уже зарегистрирован!" in str(err) or
                           "Пользователь с таким email-адресом уже существует." in str(err)
                           for err in error_messages['email'])

    @pytest.mark.parametrize("auth_user, target_user, expected_status", [
        ("user_admin", "user_admin", 200),
        ("user_admin", "user_client", 200),
        ("user_client", "user_client", 200),
        ("user_client", "user_admin", 403),
        ("anonymous_user", "user_admin", 401),
        ("anonymous_user", "user_client", 401)
    ])
    def test_user_update(self, request, api_client, auth_user, target_user, expected_status):
        """
        Тестирование редактирования пользователя
        [PATCH] http://127.0.0.1:8000/users/update/{int:pk}/
        """
        data = {"first_name": "Обновленное имя"}
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        target_user = request.getfixturevalue(target_user)

        response = client.patch(reverse('users:user_update', kwargs={'pk': target_user.pk}), data=data,
                                format='json')

        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.data["first_name"] == data["first_name"]

    @pytest.mark.parametrize("auth_user, target_user, expected_status", [
        ("user_admin", "user_admin", 204),
        ("user_admin", "user_client", 204),
        ("user_client", "user_client", 204),
        ("user_client", "user_admin", 403),
        ("anonymous_user", "user_admin", 401),
        ("anonymous_user", "user_client", 401)
    ])
    def test_user_destroy(self, request, api_client, auth_user, target_user, expected_status):
        """
        Тестирование удаления пользователя
        [DELETE] http://127.0.0.1:8000/users/delete/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        target_user = request.getfixturevalue(target_user)

        response = client.delete(reverse('users:user_delete', kwargs={'pk': target_user.pk}))

        assert response.status_code == expected_status

    @pytest.mark.parametrize("auth_user, target_user, expected_status", [
        ("user_admin", "user_admin", 200),
        ("user_admin", "user_client", 200),
        ("user_client", "user_client", 200),
        ("user_client", "user_admin", 403),
        ("anonymous_user", "user_admin", 401),
        ("anonymous_user", "user_client", 401)
    ])
    def test_user_detail(self, request, api_client, auth_user, target_user, expected_status):
        """
        Тестирование просмотра пользователя
        [GET] http://127.0.0.1:8000/users/detail/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        target_user = request.getfixturevalue(target_user)
        response = client.get(reverse('users:user_detail', kwargs={'pk': target_user.pk}))

        assert response.status_code == expected_status
        if expected_status == 200:
            expected_data = UserRetrieveSerializer(target_user).data
            if 'image' in expected_data and expected_data['image']:
                request = self.factory.get('/')
                expected_data['image'] = request.build_absolute_uri(expected_data['image'])
            assert response.data == expected_data

    @pytest.mark.parametrize("email, expected_status, expected_detail", [
        ("{user_client_email}", 200, "Ссылка для сброса пароля отправлена на почту."),
        ("not_found@example.com", 400, "Email не зарегистрирован."),
        ("invalid_email", 400, "Введите правильный адрес электронной почты.")
    ])
    def test_user_password_reset(self, api_client, user_client, email, expected_status, expected_detail):
        """
        Тестирование сброса пароля пользователя
        [POST] http://127.0.0.1:8000/users/reset_password/
        """
        if email == "{user_client_email}":
            email = self.user_client.email
        data = {"email": email}
        response = api_client.post(reverse('users:password_reset'), data=data)
        assert response.status_code == expected_status
        if expected_status == 200:
            assert response.data["detail"] == expected_detail
        else:
            if "email" in response.data:
                assert expected_detail in response.data["email"]

    @pytest.mark.parametrize("uid, token, new_password, expected_status, expected_detail", [
        ("valid_uid", "valid_token", "newpassword123", 200, "Пароль успешно сброшен!"),
        ("invalid_uid", "valid_token", "newpassword123", 400, "Невалидный UID."),
        ("valid_uid", "invalid_token", "newpassword123", 400, "Невалидный токен."),
        ("valid_uid", "valid_token", None, 400, "Обязательное поле."),

    ])
    def test_user_password_reset_confirm(self, api_client, user_client, reset_password_data, uid, token, new_password,
                                         expected_status, expected_detail):
        """
        Тестирование подтверждения сброса пароля пользователя
        [POST] http://127.0.0.1:8000/users/reset_password_confirm/{str:uid}/{str:token}/
        """
        if uid == "valid_uid":
            uid = reset_password_data["uid"]
        if token == "valid_token":
            token = reset_password_data["token"]

        data = {'uid': uid, 'token': token, "new_password": new_password} if new_password is not None else {}
        response = api_client.post(reverse('users:password_reset_confirm',
                                           kwargs={'uid': uid, 'token': token}), data=data, format='json')
        assert response.status_code == expected_status

        if expected_status == 200:
            assert response.data['detail'] == expected_detail
            self.user_client.refresh_from_db()
            assert self.user_client.check_password(new_password)
        else:
            assert expected_detail in str(response.data)


@pytest.mark.django_db
class TestUsersModel:
    """Тестирование модели приложения users"""

    def test_user_model_str(self, user_client):
        """Тестирование метода str у модели User"""
        ad = User.objects.get(pk=user_client.pk)
        assert str(ad) == user_client.email
