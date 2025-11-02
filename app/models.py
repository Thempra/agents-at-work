# app/models.py
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Integer, UUID, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(DateTime(timezone=True))
    processing_status = Column(String(50), default="pending")
    analysis_status = Column(String(50), default="pending")
    relevance_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), ForeignKey("calls.call_id"))
    analysis_result = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), ForeignKey("calls.call_id"))
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    is_sent = Column(Boolean, default=False)

Call.analyses = relationship("Analysis", back_populates="call")
Notification.call = relationship("Call", back_populates="notifications")

