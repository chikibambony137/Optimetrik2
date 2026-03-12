import pytest
from fastapi import status


def test_get_results(client, auth_headers):
    """Тест получения списка всех результатов"""
    response = client.get("/results/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_result_by_id(client, auth_headers, test_result):
    """Тест получения результата по ID"""
    response = client.get(f"/results/{test_result.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_result.id
    assert data["result_name"] == test_result.result_name


def test_get_result_not_found(client, auth_headers):
    """Тест получения несуществующего результата"""
    response = client.get("/results/99999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "не найден" in response.text


def test_create_result(client, admin_headers):
    """Тест создания нового результата администратором"""
    response = client.post("/results/", headers=admin_headers, json={
        "result_name": "Новый тестовый результат"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["result_name"] == "Новый тестовый результат"
    assert "id" in data


def test_create_result_unauthorized(client, auth_headers):
    """Тест создания результата обычным пользователем (должен быть 403)"""
    response = client.post("/results/", headers=auth_headers, json={
        "result_name": "Неавторизованный результат"
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_result_duplicate(client, admin_headers, test_result):
    """Тест создания результата с дубликатом названия"""
    response = client.post("/results/", headers=admin_headers, json={
        "result_name": test_result.result_name
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "уже существует" in response.text


def test_create_result_empty_name(client, admin_headers):
    """Тест создания результата с пустым названием"""
    response = client.post("/results/", headers=admin_headers, json={
        "result_name": ""
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_result_long_name(client, admin_headers):
    """Тест создания результата с очень длинным названием"""
    long_name = "А" * 200  # Слишком длинное название
    response = client.post("/results/", headers=admin_headers, json={
        "result_name": long_name
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_result_without_auth(client):
    """Тест создания результата без авторизации"""
    response = client.post("/results/", json={
        "result_name": "Результат без авторизации"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_results_unauthorized(client):
    """Тест получения списка результатов без авторизации"""
    response = client.get("/results/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_result_by_id_unauthorized(client, test_result):
    """Тест получения результата по ID без авторизации"""
    response = client.get(f"/results/{test_result.id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# Тесты для проверки, что результаты создаются с правильными ID в БД
def test_create_multiple_results(client, admin_headers):
    """Тест создания нескольких результатов подряд"""
    names = ["Результат 1", "Результат 2", "Результат 3"]
    created_ids = []
    
    for name in names:
        response = client.post("/results/", headers=admin_headers, json={
            "result_name": name
        })
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["result_name"] == name
        created_ids.append(data["id"])
    
    # Проверяем, что все ID разные
    assert len(set(created_ids)) == len(names)


def test_created_results_are_retrievable(client, admin_headers):
    """Тест, что созданные результаты можно получить по отдельности"""
    # Создаем результат
    create_response = client.post("/results/", headers=admin_headers, json={
        "result_name": "Тестовый результат для получения"
    })
    assert create_response.status_code == status.HTTP_201_CREATED
    result_id = create_response.json()["id"]
    
    # Получаем его по ID
    get_response = client.get(f"/results/{result_id}", headers=admin_headers)
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["id"] == result_id
    assert get_response.json()["result_name"] == "Тестовый результат для получения"


def test_results_list_includes_created(client, admin_headers):
    """Тест, что созданные результаты появляются в общем списке"""
    # Получаем текущий список
    initial_response = client.get("/results/", headers=admin_headers)
    initial_count = len(initial_response.json())
    
    # Создаем новый результат
    client.post("/results/", headers=admin_headers, json={
        "result_name": "Результат для проверки списка"
    })
    
    # Получаем обновленный список
    new_response = client.get("/results/", headers=admin_headers)
    new_count = len(new_response.json())
    
    assert new_count == initial_count + 1