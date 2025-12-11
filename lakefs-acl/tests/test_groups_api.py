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

    # Удалить
    del_resp = client.delete(f"/groups/{group_id}", headers=headers)
    assert del_resp.status_code == 204
