from sqlalchemy import Column, Integer, String, Text, Float, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default="uuid_generate_v4()")
    call_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000), nullable=False)
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default="uuid_generate_v4()")
    task_id = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    status = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default="uuid_generate_v4()")
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class CallUser(Base):
    __tablename__ = "call_user"
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class CallTask(Base):
    __tablename__ = "call_task"
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), primary_key=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True)
    status = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default="uuid_generate_v4()")
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    results = Column(JSONB)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)
