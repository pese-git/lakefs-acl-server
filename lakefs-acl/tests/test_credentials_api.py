from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"Authorization": "Bearer my-secret-key"}


def test_credential_crud_userpaths():
    # 1. Создать пользователя
    user_resp = client.post(
        "/auth/users/",
        json={"username": "creduser", "email": "creduser@example.com", "is_active": True},
        headers=headers,
    )
    assert user_resp.status_code == 201
    user_id = user_resp.json()["id"]

    # 2. Создать креденшл для пользователя (автогенерация ключей)
    create_resp = client.post(f"/auth/users/{user_id}/credentials", headers=headers)
    assert create_resp.status_code == 201
    cred = create_resp.json()
    cred_id = cred["id"]
    assert cred["user_id"] == user_id
    assert cred["access_key"] and cred["secret_key"]
    access_key = cred["access_key"]

    # 3. Листинг всех креденшлов пользователя
    list_resp = client.get(f"/auth/users/{user_id}/credentials", headers=headers)
    assert list_resp.status_code == 200
    all_creds = list_resp.json()
    assert any(c["access_key"] == access_key for c in all_creds)

    # 4. Получить креденшл по id для user
    get_c = client.get(f"/auth/users/{user_id}/credentials/{cred_id}", headers=headers)
    assert get_c.status_code == 200
    assert get_c.json()["access_key"] == access_key

    # 5. lakeFS сценарий: получить креденшл по access_key
    lakefs_c = client.get(f"/auth/credentials/{access_key}", headers=headers)
    assert lakefs_c.status_code == 200
    assert lakefs_c.json()["secret_key"] == cred["secret_key"]

    # 6. Удалить креденшл
    del_c = client.delete(f"/auth/users/{user_id}/credentials/{cred_id}", headers=headers)
    assert del_c.status_code == 204

    # 7. Проверить, что после удаления недоступен (напр. по id)
    after_del = client.get(f"/auth/users/{user_id}/credentials/{cred_id}", headers=headers)
    assert after_del.status_code == 404
