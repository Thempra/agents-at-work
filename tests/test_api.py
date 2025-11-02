import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.main import app
from app.database import Base, get_db
from app.crud import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)
from app.models import Task

# Create a test database and configure the client with it
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
testing_session = scoped_session(sessionmaker(bind=engine))

# Apply the declarative base to the test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    """Create a new database session for each test function"""
    yield testing_session
    testing_session.close()

def create_test_task(db):
    task = Task(
        call_id="test_call_id",
        name="Test Task",
        description="This is a test task.",
        url="http://example.com/test-task",
        total_funding=1000.0,
        funding_percentage=50.0,
        max_per_company=200.0,
        deadline=datetime.datetime.utcnow(),
        processing_status="pending",
        analysis_status="pending",
        relevance_score=3.5
    )
    db.add(task)
    db.commit()
    return task

def test_create_task(db):
    response = client.post(
        "/tasks/",
        json={
            "call_id": "test_call_id",
            "name": "Test Task",
            "description": "This is a test task.",
            "url": "http://example.com/test-task",
            "total_funding": 1000.0,
            "funding_percentage": 50.0,
            "max_per_company": 200.0,
            "deadline": datetime.datetime.utcnow().isoformat(),
            "processing_status": "pending",
            "analysis_status": "pending",
            "relevance_score": 3.5
        },
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["name"] == "Test Task"
    task_id = created_task["id"]
    db_task = get_task(db, task_id)
    assert db_task.name == "Test Task"

def test_read_tasks(db):
    create_test_task(db)
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0

def test_read_task(db):
    task = create_test_task(db)
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    read_task = response.json()
    assert read_task["id"] == str(task.id)

def test_update_task(db):
    task = create_test_task(db)
    update_data = {
        "name": "Updated Task",
        "description": "This is an updated task.",
        "url": "http://example.com/updated-task",
        "total_funding": 1500.0,
        "funding_percentage": 75.0,
        "max_per_company": 300.0,
        "deadline": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat(),
        "processing_status": "in_progress",
        "analysis_status": "pending",
        "relevance_score": 4.0
    }
    response = client.put(f"/tasks/{task.id}", json=update_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["name"] == "Updated Task"
    db_task = get_task(db, task.id)
    assert db_task.name == "Updated Task"

def test_delete_task(db):
    task = create_test_task(db)
    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204
    deleted_task = get_task(db, task.id)
    assert deleted_task is None

if __name__ == "__main__":
    pytest.main()
