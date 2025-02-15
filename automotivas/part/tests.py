
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from part.models import Part

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(django_user_model):
    user = django_user_model.objects.create_user(username='admin', password='secret', user_type='admin')
    return user

@pytest.fixture
def valid_csv_file():
    csv_content = "part_number,name,details,price,quantity\n"
    csv_content += "1234,Peça Teste,Detalhes da peça,100.0,10\n"
    return SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")

@pytest.fixture
def invalid_csv_file():
    csv_content = "part_number,name,details,price,quantity\n"
    csv_content += "1234,Peça Teste,Detalhes da peça,100.0,10\n"
    return SimpleUploadedFile("test.txt", csv_content.encode("utf-8"), content_type="text/plain")

@pytest.mark.django_db
def test_upload_csv_missing_file(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-upload-csv")
    response = api_client.post(url, {}, format="multipart")
    assert response.status_code == 400
    assert "Nenhum arquivo enviado" in response.data.get("detail", "")

@pytest.mark.django_db
def test_upload_csv_wrong_extension(api_client, admin_user, invalid_csv_file):
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-upload-csv")
    response = api_client.post(url, {"file": invalid_csv_file}, format="multipart")
    assert response.status_code == 400
    assert "O arquivo deve ser no formato CSV" in response.data.get("detail", "")

@pytest.mark.django_db
def test_upload_csv_valid(api_client, admin_user, valid_csv_file, monkeypatch):
    called = False

    def fake_delay(file_path):
        nonlocal called
        called = True

    monkeypatch.setattr("part.views.process_csv_file.delay", fake_delay)
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-upload-csv")
    response = api_client.post(url, {"file": valid_csv_file}, format="multipart")
    assert response.status_code == 202
    assert "Processamento iniciado" in response.data.get("detail", "")
    assert called

@pytest.mark.django_db
def test_associate_carmodels_invalid_list(api_client, admin_user):
    part = Part.objects.create(part_number="P001", name="Peça 1", details="Teste", price=100, quantity=10)
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-associate-carmodels", args=[part.pk])
    response = api_client.post(url, {"car_model_ids": "não_é_lista"}, format="json")
    assert response.status_code == 400
    assert "car_model_ids deve ser uma lista" in response.data.get("detail", "")

@pytest.mark.django_db
def test_associate_carmodels_no_car_found(api_client, admin_user):
    part = Part.objects.create(part_number="P002", name="Peça 2", details="Teste", price=200, quantity=5)
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-associate-carmodels", args=[part.pk])
    response = api_client.post(url, {"car_model_ids": [9999]}, format="json")
    assert response.status_code == 400
    assert "Nenhum CarModel encontrado" in response.data.get("detail", "")

@pytest.mark.django_db
def test_associate_carmodels_success(api_client, admin_user):
    from car.models import Car
    part = Part.objects.create(part_number="P003", name="Peça 3", details="Teste", price=300, quantity=20)
    car_model = Car.objects.create(name="ModCar1")
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-associate-carmodels", args=[part.pk])
    response = api_client.post(url, {"car_model_ids": [car_model.pk]}, format="json")
    assert response.status_code == 200
    part.refresh_from_db()
    assert car_model in part.car_models.all()

@pytest.mark.django_db
def test_disassociate_carmodel_missing_id(api_client, admin_user):
    part = Part.objects.create(part_number="P004", name="Peça 4", details="Teste", price=400, quantity=15)
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-disassociate-carmodel", args=[part.pk])
    response = api_client.post(url, {}, format="json")
    assert response.status_code == 400
    assert "car_model_id é obrigatório" in response.data.get("detail", "")

@pytest.mark.django_db
def test_disassociate_carmodel_not_found(api_client, admin_user):
    from car.models import Car
    part = Part.objects.create(part_number="P005", name="Peça 5", details="Teste", price=500, quantity=25)
    car_model = Car.objects.create(name="ModCar2")
    part.car_models.add(car_model)
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-disassociate-carmodel", args=[part.pk])
    response = api_client.post(url, {"car_model_id": 9999}, format="json")
    assert response.status_code == 404
    assert "CarModel não encontrado" in response.data.get("detail", "")

@pytest.mark.django_db
def test_disassociate_carmodel_success(api_client, admin_user):
    from car.models import Car
    part = Part.objects.create(part_number="P006", name="Peça 6", details="Teste", price=600, quantity=30)
    car_model = Car.objects.create(name="ModCar3")
    part.car_models.add(car_model)
    api_client.force_authenticate(user=admin_user)
    url = reverse("part-disassociate-carmodel", args=[part.pk])
    response = api_client.post(url, {"car_model_id": car_model.pk}, format="json")
    assert response.status_code == 200
    part.refresh_from_db()
    assert car_model not in part.car_models.all()

