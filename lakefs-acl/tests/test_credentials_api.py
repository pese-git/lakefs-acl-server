from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer my-secret-key"}

def test_create_and_get_credential():
    # Сначала создадим пользователя, иначе credential не создать
    resp = client.post("/auth/users/", json={
        "username": "creduser",
        "email": "creduser@example.com",
        "is_active": True
    }, headers=headers)
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    # Создать credentials
    response = client.post("/credentials/", json={
        "access_key": "key123",
        "secret_key": "supersecret",
        "user_id": user_id
    }, headers=headers)
    assert response.status_code == 201
    cred = response.json()
    assert cred["access_key"] == "key123"
    cred_id = cred["id"]

    # Получить по id
    get_resp = client.get(f"/credentials/{cred_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["access_key"] == "key123"

    # Листинг
    all_resp = client.get("/credentials/", headers=headers)
    assert all_resp.status_code == 200
    assert any(c["access_key"] == "key123" for c in all_resp.json())

    # Удалить
    del_resp = client.delete(f"/credentials/{cred_id}", headers=headers)
    assert del_resp.status_code == 204
