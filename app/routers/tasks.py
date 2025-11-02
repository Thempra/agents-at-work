# app/routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_task, get_tasks, create_task, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate, Task

router = APIRouter()

@router.get("/tasks/", response_model=list[Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = create_task(db=db, task=task)
        return db_task
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    try:
        updated_task = update_task(db=db, task_id=task_id, task=task)
        return updated_task
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    try:
        delete_task(db=db, task_id=task_id)
        return
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
