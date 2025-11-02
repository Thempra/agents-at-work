# tests/test_api.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, engine

# Create test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.drop_all(bind=engine_test)
    Base.metadata.create_all(bind=engine_test)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine_test)

# CRUD Operations

def test_create_call(test_db):
    response = client.post(
        "/calls/",
        json={
            "call_id": "test_rss",
            "name": "Test Call",
            "sector": "IT",
            "description": "This is a test call.",
            "url": "http://example.com/test",
            "total_funding": 1000.0,
            "funding_percentage": 50.0,
            "max_per_company": 200.0,
            "deadline": "2023-12-31T23:59:59Z",
            "processing_status": "Pending",
            "analysis_status": "Not Started",
            "relevance_score": 8.5
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"]
    call_id = data["call_id"]

    # Verify creation in database
    with test_db() as session:
        call = session.execute(text("SELECT * FROM calls WHERE call_id = :call_id"), {"call_id": call_id}).fetchone()
        assert call

def test_read_call(test_db):
    response = client.get("/calls/test_rss")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["call_id"] == "test_rss"

def test_update_call(test_db):
    response = client.put(
        "/calls/test_rss",
        json={
            "name": "Updated Test Call"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Test Call"

def test_delete_call(test_db):
    response = client.delete("/calls/test_rss")
    assert response.status_code == status.HTTP_204_NO_CONTENT

# Authentication and Error Handling (assuming JWT is implemented)

@pytest.mark.skip(reason="JWT authentication not implemented")
def test_authenticate_user():
    # Implement this test once JWT authentication is added
    pass

# Edge Cases and Validation

def test_create_call_with_missing_field(test_db):
    response = client.post(
        "/calls/",
        json={
            "name": "Test Call",
            "sector": "IT"
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
