import pytest
from fastapi import status
from datetime import date


def test_get_instruments(client, auth_headers):
    """Тест получения списка средств измерения"""
    response = client.get("/measurement-instruments/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_instrument(client, admin_headers, test_measurement_type):
    """Тест создания средства измерения"""
    response = client.post("/measurement-instruments/", headers=admin_headers, json={
        "serial_number": "TEST-SN-002",
        "date_admission": str(date.today()),
        "id_type_instrument": test_measurement_type.id
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["serial_number"] == "TEST-SN-002"


def test_create_instrument_duplicate_serial(client, admin_headers, test_instrument):
    """Тест создания с дубликатом серийного номера"""
    response = client.post("/measurement-instruments/", headers=admin_headers, json={
        "serial_number": test_instrument.serial_number,
        "date_admission": str(date.today()),
        "id_type_instrument": test_instrument.id_type_instrument
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST