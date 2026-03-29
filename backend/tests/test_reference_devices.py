from fastapi import status
from datetime import date, timedelta


def test_get_reference_devices(client, auth_headers):
    """Тест получения списка эталонов"""
    response = client.get("/reference-devices/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_reference_devices_with_valid_only(client, auth_headers, test_reference_device):
    """Тест получения эталонов с фильтром valid_only"""
    response = client.get("/reference-devices/?valid_only=true", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_reference_device_by_id(client, auth_headers, test_reference_device):
    """Тест получения эталона по ID"""
    response = client.get(f"/reference-devices/{test_reference_device.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_reference_device.id
    assert data["serial_number"] == test_reference_device.serial_number


def test_get_reference_device_not_found(client, auth_headers):
    """Тест получения несуществующего эталона"""
    response = client.get("/reference-devices/99999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_reference_device(client, admin_headers):
    """Тест создания эталона администратором"""
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
    assert data["date_admission"] == str(today)
    assert data["valid_for"] == str(valid_until)


def test_create_reference_device_unauthorized(client, auth_headers):
    """Тест создания эталона обычным пользователем (должен быть 403)"""
    today = date.today()
    valid_until = today + timedelta(days=365)

    response = client.post("/reference-devices/", headers=auth_headers, json={
        "serial_number": "REF-UNAUTH-001",
        "date_admission": str(today),
        "valid_for": str(valid_until)
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_reference_device_duplicate_serial(client, admin_headers, test_reference_device):
    """Тест создания эталона с дубликатом серийного номера"""
    today = date.today()
    valid_until = today + timedelta(days=365)

    response = client.post("/reference-devices/", headers=admin_headers, json={
        "serial_number": test_reference_device.serial_number,
        "date_admission": str(today),
        "valid_for": str(valid_until)
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "уже существует" in response.text


def test_update_reference_device(client, admin_headers, test_reference_device):
    """Тест обновления эталона"""
    new_valid_until = date.today() + timedelta(days=730)  # +2 года

    response = client.put(f"/reference-devices/{test_reference_device.id}",
                          headers=admin_headers, json={
        "valid_for": str(new_valid_until)
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["valid_for"] == str(new_valid_until)


def test_update_reference_device_unauthorized(client, auth_headers, test_reference_device):
    """Тест обновления эталона обычным пользователем (должен быть 403)"""
    response = client.put(f"/reference-devices/{test_reference_device.id}",
                          headers=auth_headers, json={
        "serial_number": "NEW-SERIAL"
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_reference_device_not_found(client, admin_headers):
    """Тест обновления несуществующего эталона"""
    response = client.put("/reference-devices/99999", headers=admin_headers, json={
        "serial_number": "NEW-SERIAL"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_reference_device(client, admin_headers, test_reference_device):
    """Тест удаления эталона"""
    response = client.delete(f"/reference-devices/{test_reference_device.id}",
                             headers=admin_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем, что эталон действительно удален
    get_response = client.get(f"/reference-devices/{test_reference_device.id}", headers=admin_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_reference_device_unauthorized(client, auth_headers, test_reference_device):
    """Тест удаления эталона обычным пользователем (должен быть 403)"""
    response = client.delete(f"/reference-devices/{test_reference_device.id}",
                             headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_reference_device_not_found(client, admin_headers):
    """Тест удаления несуществующего эталона"""
    response = client.delete("/reference-devices/99999", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_device_usage(client, auth_headers, test_reference_device):
    """Тест получения истории использования эталона"""
    response = client.get(f"/reference-devices/{test_reference_device.id}/usage", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_device_usage_not_found(client, auth_headers):
    """Тест получения истории использования несуществующего эталона"""
    response = client.get("/reference-devices/99999/usage", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
