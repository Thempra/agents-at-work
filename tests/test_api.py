# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Task, Call
from app.schemas import TaskCreate, CallCreate
from datetime import datetime

# Initialize the client and database for testing
client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the database tables before running tests
Base.metadata.create_all(bind=engine)

# Fixture to create a task for testing
@pytest.fixture
def test_task():
    task_data = {
        "id": 1,
        "task_name": "Test Task",
        "description": "A test task for API integration",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db = next(override_get_db())
    new_task = Task(**task_data)
    db.add(new_task)
    db.commit()
    yield new_task
    db.delete(new_task)
    db.commit()

# Fixture to create a call for testing
@pytest.fixture
def test_call():
    call_data = {
        "id": 1,
        "call_id": "test_call_id",
        "name": "Test Call",
        "sector": "Technology",
        "description": "A test call for API integration",
        "url": "http://example.com",
        "total_funding": 10000.0,
        "funding_percentage": 50.0,
        "max_per_company": 2000.0,
        "deadline": datetime.utcnow(),
        "processing_status": "Pending",
        "analysis_status": "Not started",
        "relevance_score": 8.5
    }
    db = next(override_get_db())
    new_call = Call(**call_data)
    db.add(new_call)
    db.commit()
    yield new_call
    db.delete(new_call)
    db.commit()

# Test for creating a task
def test_create_task(test_task):
    task_data = {
        "task_name": "Test Task",
        "description": "A test task for API integration"
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["id"] == test_task.id
    assert created_task["task_name"] == task_data["task_name"]
    assert created_task["description"] == task_data["description"]

# Test for reading a task
def test_read_task(test_task):
    response = client.get(f"/tasks/{test_task.id}")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == test_task.id
    assert task["task_name"] == test_task.task_name
    assert task["description"] == test_task.description

# Test for updating a task
def test_update_task(test_task):
    updated_data = {
        "task_name": "Updated Task",
        "description": "An updated task for API integration"
    }
    response = client.put(f"/tasks/{test_task.id}", json=updated_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["id"] == test_task.id
    assert updated_task["task_name"] == updated_data["task_name"]
    assert updated_task["description"] == updated_data["description"]

# Test for deleting a task
def test_delete_task(test_task):
    response = client.delete(f"/tasks/{test_task.id}")
    assert response.status_code == 204
    # Verify that the task has been deleted
    response = client.get(f"/tasks/{test_task.id}")
    assert response.status_code == 404

# Test for creating a call
def test_create_call(test_call):
    call_data = {
        "call_id": "test_call_id",
        "name": "Test Call",
        "sector": "Technology",
        "description": "A test call for API integration",
        "url": "http://example.com",
        "total_funding": 10000.0,
        "funding_percentage": 50.0,
        "max_per_company": 2000.0,
        "deadline": datetime.utcnow(),
        "processing_status": "Pending",
        "analysis_status": "Not started",
        "relevance_score": 8.5
    }
    response = client.post("/calls/", json=call_data)
    assert response.status_code == 201
    created_call = response.json()
    assert created_call["id"] == test_call.id
    assert created_call["call_id"] == call_data["call_id"]
    assert created_call["name"] == call_data["name"]

# Test for reading a call
def test_read_call(test_call):
    response = client.get(f"/calls/{test_call.id}")
    assert response.status_code == 200
    call = response.json()
    assert call["id"] == test_call.id
    assert call["call_id"] == test_call.call_id
    assert call["name"] == test_call.name

# Test for updating a call
def test_update_call(test_call):
    updated_data = {
        "name": "Updated Call",
        "sector": "Healthcare"
    }
    response = client.put(f"/calls/{test_call.id}", json=updated_data)
    assert response.status_code == 200
    updated_call = response.json()
    assert updated_call["id"] == test_call.id
    assert updated_call["name"] == updated_data["name"]
    assert updated_call["sector"] == updated_data["sector"]

# Test for deleting a call
def test_delete_call(test_call):
    response = client.delete(f"/calls/{test_call.id}")
    assert response.status_code == 204
    # Verify that the call has been deleted
    response = client.get(f"/calls/{test_call.id}")
    assert response.status_code == 404

# Test for error handling when accessing non-existent task/call
def test_error_handling():
    non_existent_id = 99999
    # Task error handling
    response = client.get(f"/tasks/{non_existent_id}")
    assert response.status_code == 404
    response = client.put(f"/tasks/{non_existent_id}", json={"task_name": "Non-existent task"})
    assert response.status_code == 404
    response = client.delete(f"/tasks/{non_existent_id}")
    assert response.status_code == 404

    # Call error handling
    response = client.get(f"/calls/{non_existent_id}")
    assert response.status_code == 404
    response = client.put(f"/calls/{non_existent_id}", json={"name": "Non-existent call"})
    assert response.status_code == 404
    response = client.delete(f"/calls/{non_existent_id}")
    assert response.status_code == 404

# Test for creating a task with validation errors
def test_create_task_validation_error():
    # Missing required field
    response = client.post("/tasks/", json={"task_name": "Test Task"})
    assert response.status_code == 422
    # Invalid data type
    response = client.post("/tasks/", json={"task_name": "Test Task", "description": 123})
    assert response.status_code == 422

# Test for creating a call with validation errors
def test_create_call_validation_error():
    # Missing required field
    response = client.post("/calls/", json={"call_id": "test_call_id"})
    assert response.status_code == 422
    # Invalid data type
    response = client.post("/calls/", json={"call_id": "test_call_id", "total_funding": "not a number"})
    assert response.status_code == 422

# Test for updating a task with validation errors
def test_update_task_validation_error(test_task):
    # Invalid data type
    update_data = {"description": 123}
    response = client.put(f"/tasks/{test_task.id}", json=update_data)
    assert response.status_code == 422

# Test for updating a call with validation errors
def test_update_call_validation_error(test_call):
    # Invalid data type
    update_data = {"total_funding": "not a number"}
    response = client.put(f"/calls/{test_call.id}", json=update_data)
    assert response.status_code == 422

# Test for edge cases when reading tasks/calls
def test_edge_cases():
    # Reading all tasks/calls
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) >= 1  # At least one task created by fixture

    response = client.get("/calls/")
    assert response.status_code == 200
    assert len(response.json()) >= 1  # At least one call created by fixture

# Test for edge cases when deleting tasks/calls
def test_delete_edge_cases(test_task, test_call):
    # Deleting the only task/call left
    client.delete(f"/tasks/{test_task.id}")
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 0

    client.delete(f"/calls/{test_call.id}")
    response = client.get("/calls/")
    assert response.status_code == 200
    assert len(response.json()) == 0
