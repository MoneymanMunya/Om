from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import models, security

def test_create_user(client: TestClient, db_session: Session):
    response = client.post("/users/", json={"username": "newuser", "email": "new@example.com", "password": "newpassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"

    user = db_session.query(models.User).filter(models.User.email == "new@example.com").first()
    assert user is not None
    assert security.verify_password("newpassword", user.hashed_password)

# def test_create_duplicate_user(client: TestClient, test_user):
#     # The `test_user` fixture has already created a user.
#     # Attempting to create the same user again should fail.
#     response = client.post("/users/", json=test_user)
#     assert response.status_code == 400
#     assert "already registered" in response.json()["detail"]

def test_login_for_access_token(client: TestClient, test_user):
    login_data = {"username": test_user["username"], "password": test_user["password"]}
    response = client.post("/users/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient, test_user):
    login_data = {"username": test_user["username"], "password": "wrongpassword"}
    response = client.post("/users/login", data=login_data)
    assert response.status_code == 401

def test_login_nonexistent_user(client: TestClient):
    response = client.post("/users/login", data={"username": "nosuchuser", "password": "testpassword"})
    assert response.status_code == 401

def test_read_users_me(client: TestClient, auth_headers: dict):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_read_users_me_no_token(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_read_users_me_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401
