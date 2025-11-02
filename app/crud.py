from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, UUID as sqla_UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from uuid import UUID
import datetime

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(sqla_UUID(as_uuid=True), primary_key=True, default=UUID)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(TEXT)
    url = Column(String(1000))
    total_funding = Column(Float)
    funding_percentage = Column(Float)
    max_per_company = Column(Float)
    deadline = Column(TIMESTAMP)
    processing_status = Column(String(50))
    analysis_status = Column(String(50))
    relevance_score = Column(Float)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(sqla_UUID(as_uuid=True), primary_key=True, default=UUID)
    task_id = Column(String(255), unique=True, index=True)
    description = Column(String(1000))
    status = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.datetime.utcnow)

# app/crud.py
from sqlalchemy.orm import Session
from app.models import Task, Call
from uuid import UUID
from typing import List, Optional

def get_task(db: Session, task_id: UUID):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task_data):
    try:
        task = Task(**task_data)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def update_task(db: Session, task_id: UUID, task_data):
    task = get_task(db, task_id)
    if task:
        for key, value in task_data.items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")

def delete_task(db: Session, task_id: UUID):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")
