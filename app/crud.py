from sqlalchemy import Column, Integer, String, Float, Text, UUID, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Call(Base):
    __tablename__ = "calls"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    call_id = Column(String(255), unique=True, index=True)
    name = Column(String(500))
    sector = Column(String(200))
    description = Column(Text)
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

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    status = Column(String(50))

from sqlalchemy.orm import Session
from app.schemas import CallCreate, CallUpdate

def get_call(db: Session, call_id: str):
    return db.query(Call).filter(Call.call_id == call_id).first()

def get_calls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Call).offset(skip).limit(limit).all()

def create_call(db: Session, call: CallCreate):
    db_call = Call(**call.dict())
    try:
        db.add(db_call)
        db.commit()
        db.refresh(db_call)
        return db_call
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_call(db: Session, call_id: str, call: CallUpdate):
    db_call = get_call(db, call_id)
    if not db_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    for key, value in call.dict(exclude_unset=True).items():
        setattr(db_call, key, value)
    
    try:
        db.commit()
        db.refresh(db_call)
        return db_call
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_call(db: Session, call_id: str):
    db_call = get_call(db, call_id)
    if not db_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    try:
        db.delete(db_call)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from sqlalchemy.orm import Session
from app.schemas import TaskCreate, TaskUpdate

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    try:
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        db.delete(db_task)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
