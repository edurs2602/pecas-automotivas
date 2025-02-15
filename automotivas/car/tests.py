import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from car.models import Car
from part.models import Part
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    User = get_user_model()
    return User.objects.create_user(username="admin", password="secret", user_type="admin")

@pytest.fixture
def normal_user():
    User = get_user_model()
    return User.objects.create_user(username="user", password="secret", user_type="user")

@pytest.fixture
def car_instance(admin_user):
    return Car.objects.create(name="Car1", manufacturer="Manuf", year=2020)

@pytest.fixture
def part_instance(car_instance):
    part = Part.objects.create(part_number="P001", name="Part1", details="Test", price=100, quantity=5)
    car_instance.parts.add(part)
    return part

@pytest.mark.django_db
def test_list_cars(api_client, normal_user, car_instance):
    api_client.force_authenticate(user=normal_user)
    url = reverse("car-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) >= 1

@pytest.mark.django_db
def test_create_car_as_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse("car-list")
    data = {"name": "Car2", "manufacturer": "Manuf", "year": 2021}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Car2"

@pytest.mark.django_db
def test_create_car_as_non_admin(api_client, normal_user):
    api_client.force_authenticate(user=normal_user)
    url = reverse("car-list")
    data = {"name": "Car3", "manufacturer": "Manuf", "year": 2021}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 403



