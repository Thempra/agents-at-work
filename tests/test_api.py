# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.main import app
from app.database import get_db, Base
from app.models import Call

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixtures for database setup/teardown
@pytest.fixture(autouse=True)
def init_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# CRUD Operations Tests
def test_read_calls(client):
    response = client.get("/calls/")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_create_call(client):
    payload = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "Testing Sector",
        "description": "This is a test call.",
        "url": "http://example.com/test",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
    }
    response = client.post("/calls/", json=payload)
    assert response.status_code == 201
    created_call = response.json()
    assert created_call["call_id"] == payload["call_id"]

def test_read_single_call(client):
    # Create a call to read later
    create_payload = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "Testing Sector",
        "description": "This is a test call.",
        "url": "http://example.com/test",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
    }
    client.post("/calls/", json=create_payload)
    
    response = client.get("/calls/test-call-id")
    assert response.status_code == 200
    single_call = response.json()
    assert single_call["call_id"] == create_payload["call_id"]

def test_update_call(client):
    # Create a call to update later
    create_payload = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "Testing Sector",
        "description": "This is a test call.",
        "url": "http://example.com/test",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
    }
    client.post("/calls/", json=create_payload)
    
    update_payload = {
        "name": "Updated Test Call",
        "sector": "Updated Testing Sector",
        "description": "This is an updated test call.",
        "total_funding": 2000.0,
        "funding_percentage": 75.0,
        "max_per_company": 400.0,
    }
    
    response = client.put("/calls/test-call-id", json=update_payload)
    assert response.status_code == 200
    updated_call = response.json()
    assert updated_call["name"] == update_payload["name"]

def test_delete_call(client):
    # Create a call to delete later
    create_payload = {
        "call_id": "test-call-id",
        "name": "Test Call",
        "sector": "Testing Sector",
        "description": "This is a test call.",
        "url": "http://example.com/test",
        "total_funding": 1000.0,
        "funding_percentage": 50.0,
        "max_per_company": 200.0,
        "deadline": "2023-12-31T23:59:59Z",
    }
    client.post("/calls/", json=create_payload)
    
    response = client.delete("/calls/test-call-id")
    assert response.status_code == 204
    # Verify deletion by trying to read the call again
    read_response = client.get("/calls/test-call-id")
    assert read_response.status_code == 404

# Authentication Tests (if present)
# Error Handling and Edge Cases Tests
