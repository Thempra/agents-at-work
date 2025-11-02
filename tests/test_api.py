# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base, get_db
from sqlalchemy.orm import sessionmaker
from alembic import command

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db_session(client):
    return TestingSessionLocal()
