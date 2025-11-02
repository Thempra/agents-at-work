# app/models.py

from sqlalchemy import Column, String, Integer, Float, Text, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from app.database import Base

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50), default="Pending")
    analysis_status = Column(String(50), default="Pending")
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), index=True)
    task_type = Column(String(50))
    status = Column(String(50), default="Pending")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    call = relationship("Call", back_populates="tasks")

Call.tasks = relationship("Task", order_by=Task.id, back_populates="call")
