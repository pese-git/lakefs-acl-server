from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer my-secret-key"}


def test_create_and_get_group():
    # Создать группу
    response = client.post("/groups/", json={"name": "testgroup"}, headers=headers)
    assert response.status_code == 201
    group = response.json()
    assert group["name"] == "testgroup"
    group_id = group["id"]

    # Получить по id
    get_resp = client.get(f"/groups/{group_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "testgroup"

    # Листинг
    all_resp = client.get("/groups/", headers=headers)
    assert all_resp.status_code == 200
    assert any(gr["name"] == "testgroup" for gr in all_resp.json())

    # --- Проверка опреаций с членством ---
    # Создаём пользователя
    user_resp = client.post(
        "/auth/users/",
        json={"username": "groupuser", "email": "groupuser@example.com", "is_active": True},
        headers=headers,
    )
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # Добавляем пользователя в группу
    add_resp = client.put(f"/groups/{group_id}/members/{user_id}", headers=headers)
    assert add_resp.status_code == 200
    assert user_id in [
        u["id"] for u in client.get(f"/groups/{group_id}/members", headers=headers).json()
    ]

    # Получение участников группы
    members_resp = client.get(f"/groups/{group_id}/members", headers=headers)
    assert members_resp.status_code == 200
    members = members_resp.json()
    assert any(u["id"] == user_id for u in members)

    # Удаляем пользователя из группы
    remove_resp = client.delete(f"/groups/{group_id}/members/{user_id}", headers=headers)
    assert remove_resp.status_code == 200
    members_after = client.get(f"/groups/{group_id}/members", headers=headers).json()
    assert not any(u["id"] == user_id for u in members_after)

    # Удалить группу
    del_resp = client.delete(f"/groups/{group_id}", headers=headers)
    assert del_resp.status_code == 204
