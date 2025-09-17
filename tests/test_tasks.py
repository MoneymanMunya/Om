from fastapi.testclient import TestClient

def test_unauthenticated_access(client: TestClient):
    response = client.get("/tasks/")
    assert response.status_code == 401

def test_create_task(client: TestClient, auth_headers: dict):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "owner_id" in data

def test_read_tasks(client: TestClient, auth_headers: dict):
    client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2"}, headers=auth_headers)

    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_read_single_task(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks/", json={"title": "Read Me"}, headers=auth_headers)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read Me"

def test_update_task(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks/", json={"title": "Update Me"}, headers=auth_headers)
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Title"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_task(client: TestClient, auth_headers: dict):
    create_response = client.post("/tasks/", json={"title": "Delete Me"}, headers=auth_headers)
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete_response.status_code == 200

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 404
