import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import Call
from app.crud import create_call, read_call, update_call, delete_call

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

def test_create_call(test_db):
    session = Session(bind=test_db)
    call_data = {
        "call_id": "test123",
        "name": "Test Call",
        "sector": "Technology",
        "description": "This is a test call for technology projects.",
        "url": "http://example.com/test-call",
        "total_funding": 50000.0,
        "funding_percentage": 20.0,
        "max_per_company": 10000.0,
        "deadline": "2024-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    call = create_call(session, call_data)
    assert call.call_id == call_data["call_id"]
    assert call.name == call_data["name"]
    session.close()

def test_read_call(test_db):
    session = Session(bind=test_db)
    call_data = {
        "call_id": "test123",
        "name": "Test Call",
        "sector": "Technology",
        "description": "This is a test call for technology projects.",
        "url": "http://example.com/test-call",
        "total_funding": 50000.0,
        "funding_percentage": 20.0,
        "max_per_company": 10000.0,
        "deadline": "2024-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    call = create_call(session, call_data)
    read_call_result = read_call(session, call.id)
    assert read_call_result.call_id == call_data["call_id"]
    assert read_call_result.name == call_data["name"]
    session.close()

def test_update_call(test_db):
    session = Session(bind=test_db)
    call_data = {
        "call_id": "test123",
        "name": "Test Call",
        "sector": "Technology",
        "description": "This is a test call for technology projects.",
        "url": "http://example.com/test-call",
        "total_funding": 50000.0,
        "funding_percentage": 20.0,
        "max_per_company": 10000.0,
        "deadline": "2024-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    call = create_call(session, call_data)
    update_data = {
        "name": "Updated Test Call"
    }
    updated_call = update_call(session, call.id, update_data)
    assert updated_call.name == update_data["name"]
    session.close()

def test_delete_call(test_db):
    session = Session(bind=test_db)
    call_data = {
        "call_id": "test123",
        "name": "Test Call",
        "sector": "Technology",
        "description": "This is a test call for technology projects.",
        "url": "http://example.com/test-call",
        "total_funding": 50000.0,
        "funding_percentage": 20.0,
        "max_per_company": 10000.0,
        "deadline": "2024-12-31T23:59:59Z",
        "processing_status": "Pending",
        "analysis_status": "Not Started",
        "relevance_score": 85.0
    }
    call = create_call(session, call_data)
    delete_call(session, call.id)
    with pytest.raises(HTTPException) as e:
        read_call(session, call.id)
    assert e.value.status_code == 404
    session.close()
