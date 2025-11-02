# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, Base
from app.database import SQLALCHEMY_DATABASE_URL, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_sql_app.db"

engine_test = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        return test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

# Test CRUD operations for Task model (assuming Task is defined in models.py)
from app.models import Task

def test_create_task(client):
    task_data = {
        "id": "test_id",
        "call_id": "test_rss_id",
        "name": "Test Task",
        "sector": "Technology",
        "description": "This is a test task.",
        "url": "http://example.com",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 80.0
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["id"] == task_data["id"]
    assert created_task["name"] == task_data["name"]

def test_get_task(client):
    # Assuming a task is already created in the test_db fixture
    task_id = "test_id"
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id

def test_update_task(client):
    # Assuming a task is already created in the test_db fixture
    task_id = "test_id"
    updated_data = {
        "name": "Updated Task",
        "sector": "Healthcare",
        "total_funding": 1500.0
    }
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["id"] == task_id
    assert updated_task["name"] == updated_data["name"]
    assert updated_task["sector"] == updated_data["sector"]
    assert updated_task["total_funding"] == updated_data["total_funding"]

def test_delete_task(client):
    # Assuming a task is already created in the test_db fixture
    task_id = "test_id"
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

# Test error handling (404, 400)
def test_get_nonexistent_task(client):
    non_existent_id = "non_existent_id"
    response = client.get(f"/tasks/{non_existent_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

# Test edge cases and validation
def test_create_task_missing_required_field(client):
    task_data = {
        "id": "test_id",
        "call_id": "test_rss_id",
        "name": "Test Task",
        # Missing sector field which is required
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422
