import pytest
from django.urls import reverse

from callboard.models import Ad, Review
from tests.conftest import fake


@pytest.mark.django_db
class TestAd:
    """Тестирование объявлений"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, user_admin, user_client):
        self.api_client = api_client
        self.user_admin = user_admin
        self.user_client = user_client

    @pytest.mark.parametrize("auth_user, expected_status", [
        ("user_admin", 200),
        ("user_client", 200),
        ("anonymous_user", 200),
    ])
    def test_ad_list(self, request, api_client, ads_users, auth_user, expected_status):
        """
        Тестирование просмотра списка объявлений
        [GET] http://127.0.0.1:8000/ads/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        response = client.get(reverse('ads:ad_list'))
        assert response.status_code == expected_status
        assert response.data['count'] == len(ads_users)

    @pytest.mark.parametrize("auth_user, expected_status", [
        ("user_client", 201),
        ("user_admin", 201),
        ("anonymous_user", 401)
    ])
    def test_ad_create(self, request, api_client, auth_user, expected_status):
        """
        Тестирование создания объявления
        [POST] http://127.0.0.1:8000/ads/create/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        ad_data = {
            "title": fake.sentence(nb_words=4),
            "price": fake.random_int(min=100, max=10000),
            "description": fake.text(),
        }
        response = client.post(reverse('ads:ad_create'), data=ad_data, format='json')
        assert response.status_code == expected_status
        if response.status_code == 201:
            assert response.data["title"] == ad_data["title"]
            assert response.data["price"] == ad_data["price"]
            assert response.data["description"] == ad_data["description"]

    @pytest.mark.parametrize("auth_user, expected_status", [
        ("user_admin", 200),
        ("user_client", 200),
        ("anonymous_user", 401),
    ])
    def test_ad_detail(self, request, api_client, auth_user, ads_user, expected_status):
        """
        Тестирование просмотра объявления
        [GET] http://127.0.0.1:8000/ads/detail/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        response = client.get(reverse('ads:ad_detail', kwargs={"pk": ads_user[1].pk}))
        assert response.status_code == expected_status

    @pytest.mark.parametrize("auth_user, user_ad, expected_status", [
        ("user_client", "ad_user", 200),
        ("user_client", "ad_admin", 403),
        ("user_client2", "ad_user", 403),
        ("user_client2", "ad_admin", 403),
        ("user_admin", "ad_user", 200),
        ("user_admin", "ad_admin", 200),
        ("user_admin2", "ad_user", 200),
        ("user_admin2", "ad_admin", 200),
        ("anonymous_user", "ad_user", 401),
        ("anonymous_user", "ad_admin", 401)
    ])
    def test_ad_update(self, request, api_client, auth_user, user_ad, expected_status):
        """
        Тестирование изменения объявления
        [DELETE] http://127.0.0.1:8000/ads/update/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        ad = request.getfixturevalue(user_ad)
        ad_data = {"description": fake.text()}
        response = client.patch(reverse('ads:ad_update', kwargs={"pk": ad.pk}), data=ad_data)
        assert response.status_code == expected_status
        if response.status_code == 200:
            assert response.data["description"] == ad_data["description"]

    @pytest.mark.parametrize("auth_user, user_ad, expected_status", [
        ("user_client", "ad_user", 204),
        ("user_client", "ad_admin", 403),
        ("user_client2", "ad_user", 403),
        ("user_client2", "ad_admin", 403),
        ("user_admin", "ad_user", 204),
        ("user_admin", "ad_admin", 204),
        ("user_admin2", "ad_user", 204),
        ("user_admin2", "ad_admin", 204),
        ("anonymous_user", "ad_user", 401),
        ("anonymous_user", "ad_admin", 401)
    ])
    def test_ad_destroy(self, request, api_client, auth_user, user_ad, expected_status):
        """
        Тестирование удаления объявления
        [DELETE] http://127.0.0.1:8000/ads/delete/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        ad = request.getfixturevalue(user_ad)
        response = client.delete(reverse('ads:ad_delete', kwargs={"pk": ad.pk}))
        assert response.status_code == expected_status


@pytest.mark.django_db
class TestReview:
    """Тестирование комментариев"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, user_admin, user_client):
        self.api_client = api_client
        self.user_admin = user_admin
        self.user_client = user_client

    @pytest.mark.parametrize("auth_user, review_ad, expected_status", [
        ("user_client", "ad_user", 201),
        ("user_client", "ad_admin", 201),
        ("user_admin", "ad_user", 201),
        ("user_admin", "ad_admin", 201),
        ("anonymous_user", "ad_user", 401),
        ("anonymous_user", "ad_admin", 401),
    ])
    def test_review_create(self, request, api_client, auth_user, review_ad, expected_status):
        """
        Тестирование создания комментария
        [POST] http://127.0.0.1:8000/ads/review/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        ad = request.getfixturevalue(review_ad)
        ad_data = {
            "ad": ad.pk,
            "text": fake.text(),
        }
        response = client.post(reverse('ads:review-list'), data=ad_data, format='json')
        assert response.status_code == expected_status
        if response.status_code == 200:
            assert response.data == ad_data

    @pytest.mark.parametrize("auth_user, review_ad, expected_status", [
        ("user_client", "review_user_ad", 200),
        ("user_client", "review_admin_ad", 200),
        ("user_admin", "review_user_ad", 200),
        ("user_admin", "review_admin_ad", 200),
        ("anonymous_user", "review_user_ad", 401),
        ("anonymous_user", "review_admin_ad", 401),
    ])
    def test_review_detail(self, request, api_client, auth_user, review_ad, expected_status):
        """
        Тестирование просмотра комментария
        [GET] http://127.0.0.1:8000/ads/review/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        review = request.getfixturevalue(review_ad)
        review_id = review.id
        response = client.get(reverse('ads:review-detail', kwargs={"pk": review_id}))
        assert response.status_code == expected_status

    @pytest.mark.parametrize("auth_user, expected_status", [
        ("user_client", 200),
        ("user_admin", 200),
        ("anonymous_user", 401),
    ])
    def test_review_list(self, request, api_client, auth_user, ad_with_reviews, expected_status):
        """
        Тестирование просмотра списка комментариев
        [GET] http://127.0.0.1:8000/ads/review/?ad_id={int:ad_id}
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        ad_id = ad_with_reviews.id
        response = client.get(reverse('ads:review-list'), data={'ad_id': ad_id})
        assert response.status_code == expected_status

    @pytest.mark.parametrize("auth_user, review_ad, expected_status", [
        ("user_client", "review_user_ad", 204),
        ("user_client", "review_admin_ad", 403),
        ("user_admin", "review_user_ad", 204),
        ("user_admin", "review_admin_ad", 204),
        ("anonymous_user", "review_user_ad", 401),
        ("anonymous_user", "review_admin_ad", 401),
    ])
    def test_review_destroy(self, request, api_client, auth_user, review_ad, expected_status):
        """
        Тестирование удаления комментария
        [DELETE] http://127.0.0.1:8000/ads/review/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        review = request.getfixturevalue(review_ad)
        review_id = review.id
        response = client.delete(reverse('ads:review-detail', kwargs={"pk": review_id}))
        assert response.status_code == expected_status

    @pytest.mark.parametrize("auth_user, review_ad, new_text, expected_status", [
        ("user_client", "review_user_ad", "Updated user comment", 200),
        ("user_client", "review_admin_ad", "Updated user comment", 403),
        ("user_admin", "review_user_ad", "Updated admin comment", 200),
        ("user_admin", "review_admin_ad", "Updated admin comment", 200),
        ("anonymous_user", "review_user_ad", "Updated anonymous comment", 401),
        ("anonymous_user", "review_admin_ad", "Updated anonymous comment", 401),
    ])
    def test_review_update(self, request, api_client, auth_user, review_ad, new_text, expected_status):
        """
        Тестирование изменения комментария
        [PATCH] http://127.0.0.1:8000/ads/review/{int:pk}/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        review = request.getfixturevalue(review_ad)
        review_id = review.id
        response = client.patch(
            reverse('ads:review-detail', kwargs={"pk": review_id}),
            data={'text': new_text}, format='json')
        assert response.status_code == expected_status
        if response.status_code == 200:
            review.refresh_from_db()
            assert review.text == new_text

    @pytest.mark.parametrize("auth_user, expected_status", [
        ("user_client", 400),
        ("user_admin", 400),
        ("anonymous_user", 401),
    ])
    def test_review_list_no_ad_id(self, request, api_client, auth_user, expected_status):
        """
        Тестирование получения списка комментариев без параметра ad_id
        [GET] http://127.0.0.1:8000/ads/review/
        """
        if auth_user == "anonymous_user":
            client = api_client
        else:
            user = request.getfixturevalue(auth_user)
            api_client.force_authenticate(user=user)
            client = api_client
        response = client.get(reverse('ads:review-list'))
        assert response.status_code == expected_status


@pytest.mark.django_db
class TestCallboardModels:
    """Тестирование моделей приложения callboard"""

    def test_ad_model_str(self, ad_user):
        """Тестирование метода str у модели Ad"""
        ad = Ad.objects.get(pk=ad_user.pk)
        assert str(ad) == ad_user.title

    def test_review_model_str(self, review_user_ad):
        """Тестирование метода str у модели Review"""
        ad = Review.objects.get(pk=review_user_ad.pk)
        assert str(ad) == review_user_ad.text
