from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer my-secret-key"}


def test_create_and_get_user():
    # Создание пользователя
    response = client.post(
        "/auth/users/",
        json={"username": "testuser", "email": "test@example.com", "is_active": True},
        headers=headers,
    )
    assert response.status_code == 201
    user = response.json()
    assert user["username"] == "testuser"
    user_id = user["id"]

    # Получение пользователя по id
    get_resp = client.get(f"/auth/users/{user_id}", headers=headers)
    assert get_resp.status_code == 200
    get_user = get_resp.json()
    assert get_user["username"] == "testuser"

    # Листинг
    all_users = client.get("/auth/users/", headers=headers)
    assert all_users.status_code == 200
    assert any(u["username"] == "testuser" for u in all_users.json())

    # Удаление
    del_resp = client.delete(f"/auth/users/{user_id}", headers=headers)
    assert del_resp.status_code == 204
