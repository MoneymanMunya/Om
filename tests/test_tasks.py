import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use a separate SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data
    assert "owner_id" in data

def test_read_tasks():
    # Create a task first to ensure the list is not empty
    client.post("/tasks/", json={"title": "Another Test Task", "description": "Another Test Description"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_single_task():
    # Create a task to read
    response = client.post("/tasks/", json={"title": "Read Me", "description": "A task to be read"})
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Read the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read Me"
    assert data["id"] == task_id


def test_read_nonexistent_task():
    response = client.get("/tasks/99999")
    assert response.status_code == 404


def test_update_task():
    # Create a task to update
    response = client.post("/tasks/", json={"title": "Update Me", "description": "Original Description"})
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Update the task
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Title", "description": "Updated Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"


def test_delete_task():
    # Create a task to delete
    response = client.post("/tasks/", json={"title": "Delete Me", "description": "A task to be deleted"})
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Verify it's gone
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
