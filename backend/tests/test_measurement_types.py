import pytest
from fastapi import status


def test_get_measurement_types(client, auth_headers):
    """Тест получения списка типов"""
    response = client.get("/measurement-types/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_measurement_type(client, admin_headers):
    """Тест создания типа (только админ)"""
    response = client.post("/measurement-types/", headers=admin_headers, json={
        "name_company": "Новая компания",
        "batch_number": "BATCH-001"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name_company"] == "Новая компания"
    assert data["batch_number"] == "BATCH-001"
    assert "id" in data


def test_create_measurement_type_unauthorized(client, auth_headers):
    """Тест создания типа обычным пользователем (должен быть 403)"""
    response = client.post("/measurement-types/", headers=auth_headers, json={
        "name_company": "Новая компания",
        "batch_number": "BATCH-002"
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_measurement_type_by_id(client, auth_headers, test_measurement_type):
    """Тест получения типа по ID"""
    response = client.get(f"/measurement-types/{test_measurement_type.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_measurement_type.id


def test_update_measurement_type(client, admin_headers, test_measurement_type):
    """Тест обновления типа"""
    response = client.put(f"/measurement-types/{test_measurement_type.id}", 
                          headers=admin_headers, json={
        "name_company": "Обновленная компания"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name_company"] == "Обновленная компания"


def test_delete_measurement_type(client, admin_headers, test_measurement_type):
    """Тест удаления типа"""
    response = client.delete(f"/measurement-types/{test_measurement_type.id}", 
                            headers=admin_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT