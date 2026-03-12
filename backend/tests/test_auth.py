import pytest
from fastapi import status
import uuid

def test_register_user(client):
    """Тест регистрации нового пользователя"""
    # Генерируем уникальный логин для каждого теста
    unique_login = f"newuser_{uuid.uuid4().hex[:8]}"
    
    user_data = {
        "surname": "Новый",
        "name": "Пользователь",
        "patronymic": "Тестович",
        "login": unique_login,
        "password": "NewPass123"
    }
    
    response = client.post("/auth/register", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["login"] == unique_login
    assert "password" not in data


def test_register_duplicate_login(client, test_user):
    """Тест регистрации с существующим логином"""
    response = client.post("/auth/register", json={
        "surname": "Дубль",
        "name": "Пользователь",
        "login": test_user.login,  # существующий логин
        "password": "NewPass123"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, test_user):
    """Тест успешного входа"""
    
    # Проверим пароль напрямую
    from core.security import verify_password
    is_valid = verify_password("Test123", test_user.hashed_password)
    
    response = client.post("/auth/login", data={
        "username": test_user.login,
        "password": "Test123"
    })
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Тест входа с неверным паролем"""
    response = client.post("/auth/login", data={
        "username": test_user.login,
        "password": "wrongpass"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_wrong_username(client):
    """Тест входа с неверным логином"""
    response = client.post("/auth/login", data={
        "username": "nonexistent",
        "password": "Test123"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers, test_user):
    """Тест получения информации о текущем пользователе"""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"] == test_user.login