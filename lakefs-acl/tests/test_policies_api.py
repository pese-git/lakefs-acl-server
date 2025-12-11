from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer my-secret-key"}


def test_policies_crud_and_membership():
    # Создать политику
    response = client.post(
        "/policies/", json={"name": "readonly", "document": '{"effect": "allow"}'}, headers=headers
    )
    assert response.status_code == 201
    policy = response.json()
    assert policy["name"] == "readonly"
    assert policy["document"].startswith("{")
    policy_id = policy["id"]

    # Получить по id
    get_resp = client.get(f"/policies/{policy_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "readonly"

    # Листинг
    all_resp = client.get("/policies/", headers=headers)
    assert all_resp.status_code == 200
    assert any(pl["name"] == "readonly" for pl in all_resp.json())

    # Обновление политики
    upd_resp = client.put(
        f"/policies/{policy_id}",
        json={"name": "readonly2", "document": '{"effect": "deny"}'},
        headers=headers,
    )
    assert upd_resp.status_code == 200
    assert upd_resp.json()["name"] == "readonly2"
    assert upd_resp.json()["document"] == '{"effect": "deny"}'

    # --- Тест назначения политики пользователю ---
    user_resp = client.post(
        "/auth/users/",
        json={"username": "poluser", "email": "poluser@example.com", "is_active": True},
        headers=headers,
    )
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    assign_user = client.put(f"/policies/{policy_id}/users/{user_id}", headers=headers)
    assert assign_user.status_code == 200
    assert user_id in [u["id"] for u in assign_user.json().get("users", [])]

    remove_user = client.delete(f"/policies/{policy_id}/users/{user_id}", headers=headers)
    assert remove_user.status_code == 200
    assert user_id not in [u["id"] for u in remove_user.json().get("users", [])]

    # --- Тест назначения политики группе ---
    group_resp = client.post("/groups/", json={"name": "polgroup"}, headers=headers)
    assert group_resp.status_code == 201
    group_id = group_resp.json()["id"]

    assign_group = client.put(f"/policies/{policy_id}/groups/{group_id}", headers=headers)
    assert assign_group.status_code == 200
    assert group_id in [g["id"] for g in assign_group.json().get("groups", [])]

    remove_group = client.delete(f"/policies/{policy_id}/groups/{group_id}", headers=headers)
    assert remove_group.status_code == 200
    assert group_id not in [g["id"] for g in remove_group.json().get("groups", [])]

    # Удалить
    del_resp = client.delete(f"/policies/{policy_id}", headers=headers)
    assert del_resp.status_code == 204
