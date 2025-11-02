# app/models.py
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000), nullable=False)
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(DateTime, nullable=False)
    processing_status = Column(String(50), default="Pending")
    analysis_status = Column(String(50), default="Not Started")
    relevance_score = Column(Float)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(PGUUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    call = relationship("Call", back_populates="tasks")

Call.tasks = relationship("Task", order_by=Task.id, back_populates="call")
