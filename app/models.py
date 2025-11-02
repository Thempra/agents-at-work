# app/models.py

from sqlalchemy import Column, Integer, String, Text, Float, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from uuid import uuid4
from app.database import Base

class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(Text, nullable=False)
    url = Column(String(1000), nullable=False)
    total_funding = Column(Float, nullable=False)
    funding_percentage = Column(Float, nullable=False)
    max_per_company = Column(Float, nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=False)
    processing_status = Column(String(50), nullable=False)
    analysis_status = Column(String(50), nullable=False)
    relevance_score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    # Relationships
    tasks = relationship("Task", back_populates="call")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    data = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), index=True)
    call = relationship("Call", back_populates="tasks")

# Additional models can be added here based on the requirements
