import pytest
from fastapi import status


def test_get_test_tools(client, auth_headers):
    """Тест получения списка стендов"""
    response = client.get("/test-tools/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_active_test_tools(client, auth_headers):
    """Тест получения активных стендов"""
    response = client.get("/test-tools/active", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_test_tool(client, admin_headers):
    """Тест создания стенда"""
    response = client.post("/test-tools/", headers=admin_headers, json={
        "serial_number": "TOOL-NEW-001",
        "active": True
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["serial_number"] == "TOOL-NEW-001"
    assert data["active"] is True