# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import CallCreate, CallUpdate
from app.crud import create_call, update_call, get_calls, get_call

router = APIRouter()

@router.post("/calls/", response_model=CallCreate, status_code=status.HTTP_201_CREATED)
async def create_new_task(call: CallCreate, db: Session = Depends(get_db)):
    """
    Create a new call.
    """
    return create_call(db=db, call=call)

@router.get("/calls/{call_id}", response_model=CallCreate, status_code=status.HTTP_200_OK)
async def read_task(call_id: str, db: Session = Depends(get_db)):
    """
    Get a single call by its ID.
    """
    db_call = get_call(db=db, call_id=call_id)
    if db_call is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return db_call

@router.get("/calls/", response_model=list[CallCreate], status_code=status.HTTP_200_OK)
async def read_calls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of calls.
    """
    calls = get_calls(db=db, skip=skip, limit=limit)
    return calls

@router.put("/calls/{call_id}", response_model=CallUpdate, status_code=status.HTTP_200_OK)
async def update_task(call_id: str, call: CallUpdate, db: Session = Depends(get_db)):
    """
    Update an existing call.
    """
    db_call = get_call(db=db, call_id=call_id)
    if db_call is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    return update_call(db=db, db_task=db_call, call=call)

@router.delete("/calls/{call_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(call_id: str, db: Session = Depends(get_db)):
    """
    Delete an existing call.
    """
    db_call = get_call(db=db, call_id=call_id)
    if db_call is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    db.delete(db_call)
    db.commit()
