# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate
from app.crud import create_task, update_task, get_task, get_tasks

router = APIRouter()

@router.post("/tasks/", response_model=None)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = create_task(db=db, task=task)
    return {"message": "Task created successfully", "task_id": db_task.id}

@router.get("/tasks/{task_id}", response_model=None)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task details", "task": db_task}

@router.get("/tasks/", response_model=None)
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return {"message": "List of tasks", "tasks": tasks}

@router.put("/tasks/{task_id}", response_model=None)
def update_task_status(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = update_task(db=db, task_id=task_id, task=task)
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task updated successfully", "task_id": updated_task.id}

@router.delete("/tasks/{task_id}", response_model=None)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_to_delete = get_task(db, task_id=task_id)
    if not task_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task_to_delete)
    db.commit()
    return {"message": "Task deleted successfully"}
