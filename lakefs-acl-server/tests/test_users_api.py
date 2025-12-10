import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:?cache=shared"
os.environ["ACL_API_TOKEN"] = "testtoken123"

from app.db import SessionLocal, engine
from app.models import Base

Base.metadata.create_all(bind=engine)

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer testtoken123"}


@pytest.fixture(autouse=True)
def clear_users():
    from app.models import User

    db = SessionLocal()
    db.query(User).delete()
    db.commit()
    db.close()


def test_create_user():
    resp = client.post(
        "/auth/users/",
        json={"username": "alice", "email": "alice@example.com"},
        headers=AUTH_HEADER,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert "id" in data


def test_create_user_conflict():
    client.post("/auth/users/", json={"username": "bob"}, headers=AUTH_HEADER)
    resp = client.post("/auth/users/", json={"username": "bob"}, headers=AUTH_HEADER)
    assert resp.status_code == 409


def test_list_users():
    client.post("/auth/users/", json={"username": "user1"}, headers=AUTH_HEADER)
    client.post("/auth/users/", json={"username": "user2"}, headers=AUTH_HEADER)
    resp = client.get("/auth/users/", headers=AUTH_HEADER)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    usernames = {u["username"] for u in data}
    assert "user1" in usernames and "user2" in usernames


def test_get_user_by_id():
    create_resp = client.post("/auth/users/", json={"username": "boba"}, headers=AUTH_HEADER)
    user_id = create_resp.json()["id"]
    resp = client.get(f"/auth/users/{user_id}", headers=AUTH_HEADER)
    assert resp.status_code == 200
    assert resp.json()["username"] == "boba"


def test_get_user_not_found():
    resp = client.get("/auth/users/99999", headers=AUTH_HEADER)
    assert resp.status_code == 404


def test_delete_user():
    create_resp = client.post("/auth/users/", json={"username": "deluser"}, headers=AUTH_HEADER)
    user_id = create_resp.json()["id"]
    del_resp = client.delete(f"/auth/users/{user_id}", headers=AUTH_HEADER)
    assert del_resp.status_code == 204
    # Проверяем, что пользователь удалён
    resp = client.get(f"/auth/users/{user_id}", headers=AUTH_HEADER)
    assert resp.status_code == 404


def test_auth_required():
    resp = client.get("/auth/users/")
    assert resp.status_code == 401
    resp = client.post("/auth/users/", json={"username": "charlie"})
    assert resp.status_code == 401
