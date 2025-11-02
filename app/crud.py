# app/crud.py

from sqlalchemy.orm import Session
from typing import Optional
from app.models import Call
from app.schemas import CallCreate, CallUpdate

def get_call(db: Session, call_id: str):
    return db.query(Call).filter(Call.call_id == call_id).first()

def get_calls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Call).offset(skip).limit(limit).all()

def create_call(db: Session, call: CallCreate):
    fake_hashed_password = call.url + "notreallyhashed"
    db_call = Call(
        call_id=call.call_id,
        name=call.name,
        sector=call.sector,
        description=call.description,
        url=call.url,
        total_funding=call.total_funding,
        funding_percentage=call.funding_percentage,
        max_per_company=call.max_per_company,
        deadline=call.deadline,
        processing_status="pending",
        analysis_status="pending",
        relevance_score=0.0
    )
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

def update_call(db: Session, call_id: str, call_update: CallUpdate):
    call = get_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    update_data = call_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(call, key, value)
    
    db.commit()
    db.refresh(call)
    return call

def delete_call(db: Session, call_id: str):
    call = get_call(db, call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    
    db.delete(call)
    db.commit()
    return call
