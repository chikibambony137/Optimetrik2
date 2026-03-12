import pytest
from fastapi import status
from datetime import date, timedelta


def test_create_verification(client, auth_headers, test_instrument):
    """Тест создания поверки"""
    response = client.post("/verifications/", headers=auth_headers, json={
        "planned_date_verification": str(date.today() + timedelta(days=7)),
        "date_receipt": str(date.today()),
        "id_instrument": test_instrument.id
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id_instrument"] == test_instrument.id


def test_fill_test_data(client, auth_headers, test_instrument, 
                       test_reference_device, test_test_tool):
    """Тест заполнения тестовых данных"""
    # Сначала создаем поверку
    create_response = client.post("/verifications/", headers=auth_headers, json={
        "planned_date_verification": str(date.today() + timedelta(days=7)),
        "date_receipt": str(date.today()),
        "id_instrument": test_instrument.id
    })
    verification_id = create_response.json()["id"]
    
    # Заполняем тестовые данные
    response = client.put(f"/verifications/{verification_id}/test-data", 
                         headers=auth_headers, json={
        "temperature": 23.5,
        "pressure": 1013.25,
        "wetness": 45.0,
        "complete_electric_test": True,
        "complete_voltage_test": True,
        "complete_isolation_test": True,
        "id_test_tools": [test_test_tool.id],
        "id_reference_devices": [test_reference_device.id]
    })
    assert response.status_code == status.HTTP_200_OK


def test_complete_verification(client, auth_headers, test_instrument,
                              test_reference_device, test_test_tool,
                              test_result, test_verification_type):
    """Тест завершения поверки"""
    # Создаем поверку
    create_response = client.post("/verifications/", headers=auth_headers, json={
        "planned_date_verification": str(date.today() + timedelta(days=7)),
        "date_receipt": str(date.today()),
        "id_instrument": test_instrument.id
    })
    verification_id = create_response.json()["id"]
    
    # Заполняем тестовые данные
    client.put(f"/verifications/{verification_id}/test-data", 
              headers=auth_headers, json={
        "temperature": 23.5,
        "pressure": 1013.25,
        "wetness": 45.0,
        "complete_electric_test": True,
        "complete_voltage_test": True,
        "complete_isolation_test": True,
        "id_test_tools": [test_test_tool.id],
        "id_reference_devices": [test_reference_device.id]
    })
    
    # Завершаем поверку
    response = client.put(f"/verifications/{verification_id}/complete", 
                         headers=auth_headers, json={
        "id_result": test_result.id,
        "id_type": test_verification_type.id
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["real_date_verification"] == str(date.today())