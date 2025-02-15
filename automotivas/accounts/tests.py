
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        User = get_user_model()
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.mark.django_db
def test_create_user_without_auth(api_client):
    url = reverse("user-list")
    data = {
        "username": "newuser",
        "password": "secret123",
        "email": "newuser@example.com"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["username"] == "newuser"

@pytest.mark.django_db
def test_list_users_requires_auth(api_client, create_user):
    user = create_user(username="testuser", password="secret", email="test@example.com", user_type="regular")
    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code in [401, 403]

@pytest.mark.django_db
def test_list_users_with_auth(api_client, create_user):
    user = create_user(username="testuser", password="secret", email="test@example.com", user_type="regular")
    api_client.force_authenticate(user=user)
    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == 200
    if isinstance(response.data, dict) and "results" in response.data:
        results = response.data["results"]
    else:
        results = response.data
    assert isinstance(results, list)

@pytest.mark.django_db
def test_retrieve_user_requires_auth(api_client, create_user):
    user = create_user(username="testuser", password="secret", email="test@example.com", user_type="regular")
    url = reverse("user-detail", args=[user.pk])
    response = api_client.get(url)
    assert response.status_code in [401, 403]

@pytest.mark.django_db
def test_retrieve_user_with_auth(api_client, create_user):
    user = create_user(username="testuser", password="secret", email="test@example.com", user_type="regular")
    api_client.force_authenticate(user=user)
    url = reverse("user-detail", args=[user.pk])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["username"] == user.username

@pytest.mark.django_db
def test_update_user_requires_auth(api_client, create_user):
    user = create_user(username="testuser", password="secret", email="test@example.com", user_type="regular")
    url = reverse("user-detail", args=[user.pk])
    data = {"username": "updateduser"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code in [401, 403]

@pytest.mark.django_db
def test_update_user_with_auth(api_client, create_user):
    user = create_user(username="testuser", password="secret", email="test@example.com", user_type="regular")
    api_client.force_authenticate(user=user)
    url = reverse("user-detail", args=[user.pk])
    data = {"username": "updateduser"}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == 200
    assert response.data["username"] == "updateduser"

