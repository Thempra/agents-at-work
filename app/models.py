from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Call(Base):
    __tablename__ = 'calls'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
    url = Column(String(1000), unique=True, index=True)
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

# Assuming there's another model 'User' for the relationship
class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, index=True)
    password_hash = Column(String(256))
    calls = relationship('Call', secondary='user_calls')

# Assuming there's a junction table for many-to-many relationship between User and Call
class UserCall(Base):
    __tablename__ = 'user_calls'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    call_id = Column(UUID(as_uuid=True), ForeignKey('calls.id'), primary_key=True)
