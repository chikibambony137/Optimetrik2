import pytest
from fastapi import status


def test_get_users(client, auth_headers):
    """Тест получения списка пользователей"""
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_user_by_id(client, auth_headers, test_user):
    """Тест получения пользователя по ID"""
    response = client.get(f"/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["login"] == test_user.login


def test_get_user_not_found(client, auth_headers):
    """Тест получения несуществующего пользователя"""
    response = client.get("/users/99999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_user_by_admin(client, admin_headers):
    """Тест создания пользователя администратором"""
    response = client.post("/users/", headers=admin_headers, json={
        "surname": "Созданный",
        "name": "Админом",
        "patronymic": "Тестович",
        "login": "createdbyadmin",
        "password": "Admin123",
        "admin_role": False
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["login"] == "createdbyadmin"
    assert data["admin_role"] is False


def test_update_user(client, auth_headers, test_user):
    """Тест обновления пользователя"""
    response = client.put(f"/users/{test_user.id}", headers=auth_headers, json={
        "surname": "Обновленная",
        "name": "Фамилия"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["surname"] == "Обновленная"
    assert data["name"] == "Фамилия"


def test_delete_user(client, admin_headers, test_user):
    """Тест удаления пользователя"""
    response = client.delete(f"/users/{test_user.id}", headers=admin_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Проверяем, что пользователь действительно удален
    get_response = client.get(f"/users/{test_user.id}", headers=admin_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND