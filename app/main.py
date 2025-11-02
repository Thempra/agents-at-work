# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks
from app.schemas import CallCreate, CallUpdate

app = FastAPI(
    title="Call for Tenders API",
    description="API para el monitoreo y análisis de convocatorias de la Unión Europea",
    version="1.0.0",
)

# Configure CORS (permissive for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database and create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(tasks.router)

# Health check endpoint
@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

# Startup/shutdown events for database
@app.on_event("startup")
async def startup_db():
    try:
        db = SessionLocal()
        # Perform any initialization or migration logic here
        db.close()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
async def shutdown_db():
    db = SessionLocal(bind=engine)
    db.close()

# Example endpoint for creating a new call
@app.post("/calls/", response_model=CallCreate, tags=["Calls"])
def create_call(call: CallCreate, db: Session = Depends(get_db)):
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
    )
    db.add(db_call)
    db.commit()
    db.refresh(db_call)
    return db_call

# Example endpoint for retrieving a single call
@app.get("/calls/{call_id}", response_model=CallCreate, tags=["Calls"])
def read_call(call_id: str, db: Session = Depends(get_db)):
    db_call = get_call(db=db, call_id=call_id)
    if db_call is None:
        raise HTTPException(status_code=404, detail="Call not found")
    return db_call

# Example endpoint for retrieving all calls
@app.get("/calls/", response_model=list[CallCreate], tags=["Calls"])
def read_calls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_calls = get_calls(db=db, skip=skip, limit=limit)
    return db_calls
