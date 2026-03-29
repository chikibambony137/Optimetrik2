from fastapi import status


def test_get_current_user(client, auth_headers, test_user):
    """Тест получения информации о текущем пользователе"""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["login"] == test_user.login
    assert data["surname"] == test_user.surname
    assert data["name"] == test_user.name


def test_get_current_user_unauthorized(client):
    """Тест получения информации о текущем пользователе без авторизации"""
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_users_as_admin(client, admin_headers):
    """Тест получения списка пользователей администратором"""
    response = client.get("/users/", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_users_as_regular_user(client, auth_headers):
    """Тест получения списка пользователей обычным пользователем (должен быть 403)"""
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_by_id_as_admin(client, admin_headers, test_user):
    """Тест получения пользователя по ID администратором"""
    response = client.get(f"/users/{test_user.id}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["login"] == test_user.login


def test_get_user_by_id_as_regular_user(client, auth_headers, test_user):
    """Тест получения пользователя по ID обычным пользователем (должен быть 403)"""
    response = client.get(f"/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_not_found_as_admin(client, admin_headers):
    """Тест получения несуществующего пользователя администратором"""
    response = client.get("/users/99999", headers=admin_headers)
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
    assert "id" in data


def test_create_user_by_regular_user(client, auth_headers):
    """Тест создания пользователя обычным пользователем (должен быть 403)"""
    response = client.post("/users/", headers=auth_headers, json={
        "surname": "Обычный",
        "name": "Пользователь",
        "login": "regularuser",
        "password": "Test123",
        "admin_role": False
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_duplicate_login(client, admin_headers, test_user):
    """Тест создания пользователя с дубликатом логина"""
    response = client.post("/users/", headers=admin_headers, json={
        "surname": "Дубль",
        "name": "Пользователь",
        "login": test_user.login,
        "password": "Test123",
        "admin_role": False
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "уже существует" in response.text


def test_update_user_as_admin(client, admin_headers, test_user):
    """Тест обновления пользователя администратором"""
    response = client.put(f"/users/{test_user.id}", headers=admin_headers, json={
        "surname": "Обновлено админом",
        "name": "Новое имя"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["surname"] == "Обновлено админом"
    assert data["name"] == "Новое имя"


def test_update_user_as_regular_user(client, auth_headers, test_user):
    """Тест обновления пользователя обычным пользователем (должен быть 403)"""
    response = client.put(f"/users/{test_user.id}", headers=auth_headers, json={
        "surname": "Хакер"
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_user_duplicate_login(client, admin_headers, test_user, test_admin):
    """Тест обновления пользователя с дубликатом логина"""
    response = client.put(f"/users/{test_user.id}", headers=admin_headers, json={
        "login": test_admin.login
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "уже существует" in response.text


def test_update_user_not_found(client, admin_headers):
    """Тест обновления несуществующего пользователя"""
    response = client.put("/users/99999", headers=admin_headers, json={
        "surname": "Новый"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_as_admin(client, admin_headers, test_user):
    """Тест удаления пользователя администратором"""
    response = client.delete(f"/users/{test_user.id}", headers=admin_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Проверяем, что пользователь действительно удален
    get_response = client.get(f"/users/{test_user.id}", headers=admin_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_as_regular_user(client, auth_headers, test_user):
    """Тест удаления пользователя обычным пользователем (должен быть 403)"""
    response = client.delete(f"/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_self_as_admin(client, admin_headers, test_admin):
    """Тест попытки удалить самого себя (должен быть 400)"""
    response = client.delete(f"/users/{test_admin.id}", headers=admin_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Нельзя удалить свою учетную запись" in response.text


def test_delete_user_not_found(client, admin_headers):
    """Тест удаления несуществующего пользователя"""
    response = client.delete("/users/99999", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_change_password_success(client, auth_headers, test_user):
    """Тест успешной смены пароля"""
    response = client.post("/users/change-password", headers=auth_headers, json={
        "current_password": "Test123",
        "new_password": "NewPass456"
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Пароль успешно изменен"

    # Проверяем, что новый пароль работает
    from core.security import verify_password
    db_user = test_user  # тестовый пользователь из фикстуры
    assert verify_password("NewPass456", db_user.hashed_password)


def test_change_password_wrong_current(client, auth_headers, test_user):
    """Тест смены пароля с неверным текущим паролем"""
    response = client.post("/users/change-password", headers=auth_headers, json={
        "current_password": "WrongPass",
        "new_password": "NewPass456"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Неверный текущий пароль" in response.text


def test_change_password_too_short(client, auth_headers, test_user):
    """Тест смены пароля на слишком короткий"""
    response = client.post("/users/change-password", headers=auth_headers, json={
        "current_password": "Test123",
        "new_password": "123"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "минимум 6 символов" in response.text


def test_change_password_unauthorized(client):
    """Тест смены пароля без авторизации"""
    response = client.post("/users/change-password", json={
        "current_password": "Test123",
        "new_password": "NewPass456"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
