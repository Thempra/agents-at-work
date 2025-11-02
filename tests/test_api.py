import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Call, Task
from app.schemas import CallCreate, CallUpdate

# Initialize FastAPI application and client
app = FastAPI()
client = TestClient(app)

# Mock data for testing
test_call_data = {
    "call_id": "test-call-123",
    "name": "Test Call 1",
    "sector": "IT",
    "description": "A test call for IT projects.",
    "url": "http://example.com/test-call",
    "total_funding": 100000.0,
    "funding_percentage": 50.0,
    "max_per_company": 10000.0,
    "deadline": datetime.utcnow(),
    "processing_status": "Pending",
    "analysis_status": "Not Started",
    "relevance_score": 80.0
}

# Fixtures for database setup/teardown
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    yield SessionLocal()
    Base.metadata.drop_all(bind=engine)

# Test create_call endpoint
def test_create_call(db: Session):
    response = client.post("/calls/", json=test_call_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 201
    created_call = Call(**response.json())
    assert created_call.call_id == test_call_data["call_id"]
    assert created_call.name == test_call_data["name"]

# Test get_calls endpoint
def test_get_calls(db: Session):
    client.post("/calls/", json=test_call_data, headers={"Content-Type": "application/json"})
    response = client.get("/calls/")
    assert response.status_code == 200
    calls = response.json()
    assert len(calls) >= 1
    first_call = Call(**calls[0])
    assert first_call.call_id == test_call_data["call_id"]

# Test get_call endpoint
def test_get_call(db: Session):
    client.post("/calls/", json=test_call_data, headers={"Content-Type": "application/json"})
    response = client.get(f"/calls/{test_call_data['call_id']}")
    assert response.status_code == 200
    call = Call(**response.json())
    assert call.call_id == test_call_data["call_id"]

# Test update_call endpoint
def test_update_call(db: Session):
    client.post("/calls/", json=test_call_data, headers={"Content-Type": "application/json"})
    updated_data = {
        "name": "Updated Test Call",
        "description": "An updated test call for IT projects."
    }
    response = client.put(f"/calls/{test_call_data['call_id']}", json=updated_data)
    assert response.status_code == 200
    updated_call = Call(**response.json())
    assert updated_call.name == updated_data["name"]

# Test delete_call endpoint
def test_delete_call(db: Session):
    client.post("/calls/", json=test_call_data, headers={"Content-Type": "application/json"})
    response = client.delete(f"/calls/{test_call_data['call_id']}")
    assert response.status_code == 204
