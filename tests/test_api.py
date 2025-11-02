import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from app.main import app
from app.database import engine, Base, SessionLocal
from app.routers.tasks import router as tasks_router
from app.crud import create_task, get_task, update_task, delete_task
from app.models import Task

# Fixture to setup the database for tests
@pytest.fixture(scope="module")
def test_db():
    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Drop all tables from the test database
    Base.metadata.drop_all(bind=engine)

# Fixture to create a TestClient instance
@pytest.fixture
def client(test_db):
    return TestClient(app)

# Test for creating a new task
def test_create_task(client: TestClient, test_db):
    task_data = {
        "call_id": "test_call_id",
        "name": "Test Task",
        "sector": "Test Sector",
        "description": "This is a test task.",
        "url": "http://example.com/test-task",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Analyzed",
        "relevance_score": 80.0
    }
    
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = response.json()
    assert created_task["call_id"] == task_data["call_id"]
    assert created_task["name"] == task_data["name"]

# Test for getting a task by ID
def test_get_task(client: TestClient, test_db):
    task_data = {
        "call_id": "test_call_id",
        "name": "Test Task",
        "sector": "Test Sector",
        "description": "This is a test task.",
        "url": "http://example.com/test-task",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Analyzed",
        "relevance_score": 80.0
    }
    
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = response.json()
    
    task_id = created_task["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id

# Test for updating a task
def test_update_task(client: TestClient, test_db):
    task_data = {
        "call_id": "test_call_id",
        "name": "Test Task",
        "sector": "Test Sector",
        "description": "This is a test task.",
        "url": "http://example.com/test-task",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Analyzed",
        "relevance_score": 80.0
    }
    
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = response.json()
    
    task_id = created_task["id"]
    updated_data = {
        "name": "Updated Test Task"
    }
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    updated_task = response.json()
    assert updated_task["id"] == task_id
    assert updated_task["name"] == updated_data["name"]

# Test for deleting a task
def test_delete_task(client: TestClient, test_db):
    task_data = {
        "call_id": "test_call_id",
        "name": "Test Task",
        "sector": "Test Sector",
        "description": "This is a test task.",
        "url": "http://example.com/test-task",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Analyzed",
        "relevance_score": 80.0
    }
    
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = response.json()
    
    task_id = created_task["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

# Test for getting all tasks with pagination
def test_get_tasks(client: TestClient, test_db):
    for i in range(5):  # Create 5 tasks
        task_data = {
            "call_id": f"test_call_id_{i}",
            "name": f"Test Task {i}",
            "sector": "Test Sector",
            "description": "This is a test task.",
            "url": "http://example.com/test-task",
            "total_funding": 1000.0,
            "funding_percentage": 50.0,
            "max_per_company": 200.0,
            "deadline": "2023-12-31T23:59:59Z",
            "processing_status": "Pending",
            "analysis_status": "Not Analyzed",
            "relevance_score": 80.0
        }
        
        client.post("/tasks/", json=task_data)
    
    response = client.get("/tasks/?skip=0&limit=3")
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) == 3

# Test for error handling: getting a non-existent task
def test_get_non_existent_task(client: TestClient, test_db):
    response = client.get("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Test for error handling: creating a task with invalid data
def test_create_task_with_invalid_data(client: TestClient, test_db):
    invalid_task_data = {
        "call_id": None,
        "name": "",
        "sector": None,
        "description": None,
        "url": "",
        "total_funding": None,
        "funding_percentage": None,
        "max_per_company": None,
        "deadline": None,
        "processing_status": None,
        "analysis_status": None,
        "relevance_score": None
    }
    
    response = client.post("/tasks/", json=invalid_task_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# Test for error handling: updating a task with invalid data
def test_update_task_with_invalid_data(client: TestClient, test_db):
    task_data = {
        "call_id": "test_call_id",
        "name": "Test Task",
        "sector": "Test Sector",
        "description": "This is a test task.",
        "url": "http://example.com/test-task",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Analyzed",
        "relevance_score": 80.0
    }
    
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_task = response.json()
    
    task_id = created_task["id"]
    invalid_update_data = {
        "name": None,
        "sector": "",
        "description": None,
        "url": None,
        "total_funding": None,
        "funding_percentage": None,
        "max_per_company": None,
        "deadline": None,
        "processing_status": None,
        "analysis_status": None,
        "relevance_score": None
    }
    
    response = client.put(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# Test for error handling: deleting a non-existent task
def test_delete_non_existent_task(client: TestClient, test_db):
    response = client.delete("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
