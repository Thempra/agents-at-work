import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base, engine
from app.models import Task, Call

# Create an in-memory database for testing purposes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal_test = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

app.dependency_overrides[get_db] = lambda: SessionLocal_test()

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks/",
        json={"name": "Test Task", "sector": "IT", "description": "A test task"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Task"
    assert data["sector"] == "IT"
    assert data["description"] == "A test task"


def test_read_task():
    # Create a task to read
    client.post(
        "/tasks/",
        json={"name": "Read Task", "sector": "HR", "description": "A task to read"},
    )
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Read Task"


def test_update_task():
    # Create a task to update
    response = client.post(
        "/tasks/",
        json={"name": "Update Task", "sector": "Legal", "description": "A task to update"},
    )
    task_id = response.json()["id"]
    updated_data = {"name": "Updated Name", "description": "Updated Description"}
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated Description"


def test_delete_task():
    # Create a task to delete
    response = client.post(
        "/tasks/",
        json={"name": "Delete Task", "sector": "Marketing", "description": "A task to delete"},
    )
    task_id = response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204


def test_read_nonexistent_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404
