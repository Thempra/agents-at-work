import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Create a temporary in-memory database for testing purposes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Call(Base):
    __tablename__ = 'calls'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500))
    description = Column(Text)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Fixture for creating a test session
@pytest.fixture(scope="module")
def db_session():
    session = SessionLocal()
    yield session
    session.close()

# Test fixture to create a sample call record in the database
@pytest.fixture(scope="function")
def test_call(db_session):
    new_call = Call(name="Test Call", description="This is a test call.")
    db_session.add(new_call)
    db_session.commit()
    db_session.refresh(new_call)
    yield new_call
    db_session.delete(new_call)
    db_session.commit()

# Test creating a new call
def test_create_call(db_session):
    new_call = Call(name="New Call", description="This is a new call.")
    db_session.add(new_call)
    db_session.commit()
    assert new_call.id is not None
    assert new_call.name == "New Call"
    assert new_call.description == "This is a new call."

# Test reading a call by ID
def test_read_call(test_call, db_session):
    call = db_session.query(Call).filter(Call.id == test_call.id).first()
    assert call.id == test_call.id
    assert call.name == test_call.name
    assert call.description == test_call.description

# Test updating a call
def test_update_call(test_call, db_session):
    updated_name = "Updated Call"
    updated_description = "This is an updated call."
    
    test_call.name = updated_name
    test_call.description = updated_description
    db_session.commit()
    
    updated_call = db_session.query(Call).filter(Call.id == test_call.id).first()
    assert updated_call.name == updated_name
    assert updated_call.description == updated_description

# Test deleting a call
def test_delete_call(test_call, db_session):
    db_session.delete(test_call)
    db_session.commit()
    
    deleted_call = db_session.query(Call).filter(Call.id == test_call.id).first()
    assert deleted_call is None

# Test handling 404 error for non-existent call
def test_read_non_existent_call(db_session):
    with pytest.raises(HTTPException) as exc_info:
        call = db_session.query(Call).filter(Call.id == 999).first()
        assert exc_info.value.status_code == 404

# Test validation errors for empty name
def test_create_call_with_empty_name(db_session):
    new_call = Call(name="", description="This is a test call.")
    with pytest.raises(HTTPException) as exc_info:
        db_session.add(new_call)
        db_session.commit()
        assert exc_info.value.status_code == 400

# Test validation errors for long name
def test_create_call_with_long_name(db_session):
    long_name = "a" * 501  # Exceeds VARCHAR(500) limit
    new_call = Call(name=long_name, description="This is a test call.")
    with pytest.raises(HTTPException) as exc_info:
        db_session.add(new_call)
        db_session.commit()
        assert exc_info.value.status_code == 400

# Test validation errors for empty description
def test_create_call_with_empty_description(db_session):
    new_call = Call(name="Test Call", description="")
    with pytest.raises(HTTPException) as exc_info:
        db_session.add(new_call)
        db_session.commit()
        assert exc_info.value.status_code == 400

# Test validation errors for long description
def test_create_call_with_long_description(db_session):
    long_description = "a" * 65536  # Exceeds TEXT limit
    new_call = Call(name="Test Call", description=long_description)
    with pytest.raises(HTTPException) as exc_info:
        db_session.add(new_call)
        db_session.commit()
        assert exc_info.value.status_code == 400

# Test edge case: updating a non-existent call
def test_update_non_existent_call(db_session):
    updated_name = "Updated Call"
    updated_description = "This is an updated call."
    
    with pytest.raises(HTTPException) as exc_info:
        call = Call(name=updated_name, description=updated_description)
        db_session.merge(call)
        db_session.commit()
        assert exc_info.value.status_code == 404

# Test edge case: deleting a non-existent call
def test_delete_non_existent_call(db_session):
    with pytest.raises(HTTPException) as exc_info:
        call = Call(id=999)
        db_session.delete(call)
        db_session.commit()
        assert exc_info.value.status_code == 404

