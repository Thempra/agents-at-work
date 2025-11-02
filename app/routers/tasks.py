# app/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_task, delete_task, get_task, get_tasks, update_task
from app.models import Task
from uuid import UUID
from typing import List, Optional

router = APIRouter()

@router.get("/tasks/", response_model=List[Task], status_code=status.HTTP_200_OK)
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(task: Task, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@router.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task_endpoint(task_id: UUID, task_data: dict, db: Session = Depends(get_db)):
    task = update_task(db=db, task_id=task_id, task_data=task_data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    if not delete_task(db=db, task_id=task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
