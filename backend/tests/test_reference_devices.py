import pytest
from fastapi import status
from datetime import date, timedelta


def test_get_reference_devices(client, auth_headers):
    """Тест получения списка эталонов"""
    response = client.get("/reference-devices/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_valid_reference_devices(client, auth_headers):
    """Тест получения только валидных эталонов"""
    response = client.get("/reference-devices/valid", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_reference_device(client, admin_headers):
    """Тест создания эталона"""
    today = date.today()
    valid_until = today + timedelta(days=365)
    
    response = client.post("/reference-devices/", headers=admin_headers, json={
        "serial_number": "REF-NEW-001",
        "date_admission": str(today),
        "valid_for": str(valid_until)
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["serial_number"] == "REF-NEW-001"