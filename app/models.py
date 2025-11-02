from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, UUID, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from uuid import uuid4

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500), nullable=False)
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP(timezone=True))
    processing_status = Column(String(50), nullable=False)
    analysis_status = Column(String(50), nullable=False)
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_type = Column(String(50), nullable=False)
    data = Column(JSONB)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

class CallAnalysis(Base):
    __tablename__ = "call_analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    call_id = Column(UUID(as_uuid=True), ForeignKey("calls.id"), nullable=False)
    analysis_result = Column(JSONB)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

Call.analyses = relationship(
    "CallAnalysis",
    backref=backref("call", lazy="joined"),
    cascade="all, delete-orphan",
    order_by=CallAnalysis.id
)

Task.call = relationship(
    "Call",
    backref=backref("tasks", lazy="joined"),
    foreign_keys=[Task.data["call_id"]],
    uselist=False,
)
