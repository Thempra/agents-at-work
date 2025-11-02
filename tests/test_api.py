# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base, get_db

# Initialize the client and clear the database before each test
@pytest.fixture(scope="module")
def client():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client

# CRUD operations tests
def test_create_task(client):
    response = client.post("/tasks/", json={"name": "Test Task", "description": "Test Description", "status": "Pending", "due_date": "2023-12-31T23:59:59"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Task"
    task_id = data["id"]

def test_read_task(client):
    # Create a task first
    client.post("/tasks/", json={"name": "Task for Read", "description": "Description for Read", "status": "Completed", "due_date": "2023-11-30T23:59:59"})
    
    response = client.get("/tasks/1")  # Assuming the first task created has id 1
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Task for Read"

def test_update_task(client):
    # Create a task first
    client.post("/tasks/", json={"name": "Task for Update", "description": "Description for Update", "status": "Pending", "due_date": "2023-12-01T23:59:59"})
    
    response = client.put("/tasks/1", json={"name": "Updated Task", "description": "Updated Description", "status": "Completed"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Task"

def test_delete_task(client):
    # Create a task first
    client.post("/tasks/", json={"name": "Task for Delete", "description": "Description for Delete", "status": "Pending", "due_date": "2023-12-02T23:59:59"})
    
    response = client.delete("/tasks/1")  # Assuming the first task created has id 1
    assert response.status_code == 204

# Error handling tests
def test_read_nonexistent_task(client):
    response = client.get("/tasks/100")
    assert response.status_code == 404

def test_create_task_invalid_data(client):
    response = client.post("/tasks/", json={"name": "", "description": ""})
    assert response.status_code == 422
