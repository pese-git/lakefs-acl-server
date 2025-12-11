from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer my-secret-key"}

def test_create_and_get_policy():
    # Создать политику
    response = client.post("/policies/", json={"name": "readonly", "document": '{"effect": "allow"}'}, headers=headers)
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

    # Удалить
    del_resp = client.delete(f"/policies/{policy_id}", headers=headers)
    assert del_resp.status_code == 204
