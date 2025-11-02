from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import create_task, read_task, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate

router = APIRouter()

@router.post("/tasks/", response_model=TaskCreate, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@router.get("/tasks/{task_id}", response_model=TaskCreate)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = read_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@router.get("/tasks/", response_model=list[TaskCreate])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = read_tasks(db, skip=skip, limit=limit)
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskUpdate)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = update_task(db=db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"detail": "Task deleted"}
