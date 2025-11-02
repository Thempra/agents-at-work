from sqlalchemy.orm import Session
from typing import Optional
from app.models import Call, Task  # Assuming there is a Task model similar to Call
from app.schemas import CallCreate, CallUpdate, TaskCreate, TaskUpdate

# CRUD operations for Call
def get_call(db: Session, call_id: int):
    return db.query(Call).filter(Call.id == call_id).first()

def get_calls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Call).offset(skip).limit(limit).all()

def create_call(db: Session, call: CallCreate):
    fake_hashed_password = call.description + "notreallyhashed"
    db_call = Call(
        id=call.id,
        call_id=call.call_id,
        name=call.name,
        sector=call.sector,
        description=call.description,
        url=call.url,
        total_funding=call.total_funding,
        funding_percentage=call.funding_percentage,
        max_per_company=call.max_per_company,
        deadline=call.deadline,
        processing_status=call.processing_status,
        analysis_status=call.analysis_status,
        relevance_score=call.relevance_score
    )
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

def update_call(db: Session, call_id: int, call_update: CallUpdate):
    db_call = db.query(Call).filter(Call.id == call_id).first()
    if not db_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    for key, value in call_update.dict(exclude_unset=True).items():
        setattr(db_call, key, value)
    
    db.commit()
    db.refresh(db_call)
    return db_call

def delete_call(db: Session, call_id: int):
    db_call = db.query(Call).filter(Call.id == call_id).first()
    if not db_call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    db.delete(db_call)
    db.commit()
    return db_call

# CRUD operations for Task
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate):
    fake_hashed_password = task.name + "notreallyhashed"
    db_task = Task(
        id=task.id,
        name=task.name,
        description=task.description
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return db_task
