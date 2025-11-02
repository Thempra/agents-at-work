from sqlalchemy import Column, Integer, String, Float, Text, UUID, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    task_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=datetime.utcnow)

# Other models can be defined here
