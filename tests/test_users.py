import pytest
from fastapi.testclient import TestClient

import main


TEST_AUTH = ("test-user", "test-password")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("API_USERNAME", TEST_AUTH[0])
    monkeypatch.setenv("API_PASSWORD", TEST_AUTH[1])
    monkeypatch.setattr(main, "DATABASE_PATH", tmp_path / "test_users.db")
    main.initialize_database()

    with TestClient(main.app) as test_client:
        yield test_client


def test_users_endpoints_require_basic_auth(client):
    response = client.get("/users")

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Basic"

    invalid_credentials = client.get(
        "/users",
        auth=("wrong-user", "wrong-password"),
    )
    assert invalid_credentials.status_code == 401


def test_users_crud_flow(client):
    created = client.post(
        "/users",
        auth=TEST_AUTH,
        json={"name": "  Alex Student  ", "email": "alex@example.com"},
    )
    assert created.status_code == 201
    user = created.json()
    assert user["name"] == "Alex Student"
    assert user["email"] == "alex@example.com"

    listed = client.get("/users", auth=TEST_AUTH)
    assert listed.status_code == 200
    assert listed.json() == [user]

    updated = client.put(
        f"/users/{user['id']}",
        auth=TEST_AUTH,
        json={"name": "Alex S.", "email": "alex.s@example.com"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Alex S."
    assert updated.json()["email"] == "alex.s@example.com"

    deleted = client.delete(f"/users/{user['id']}", auth=TEST_AUTH)
    assert deleted.status_code == 204
    assert client.get("/users", auth=TEST_AUTH).json() == []


def test_invalid_email_is_rejected(client):
    response = client.post(
        "/users",
        auth=TEST_AUTH,
        json={"name": "Alex Student", "email": "not-an-email"},
    )

    assert response.status_code == 422


def test_duplicate_email_is_rejected(client):
    payload = {"name": "Alex Student", "email": "alex@example.com"}
    first = client.post("/users", auth=TEST_AUTH, json=payload)
    duplicate = client.post("/users", auth=TEST_AUTH, json=payload)

    assert first.status_code == 201
    assert duplicate.status_code == 409


def test_update_missing_user_returns_404(client):
    response = client.put(
        "/users/999",
        auth=TEST_AUTH,
        json={"name": "Alex Student", "email": "alex@example.com"},
    )

    assert response.status_code == 404
