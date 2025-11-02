# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router

app = FastAPI(
    title="Call for Tenders API",
    version="1.0.0",
    description="API for managing tender calls from the European Union."
)

# CORS Configuration (permissive for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Initialization
Base.metadata.create_all(bind=engine)

# Include router from tasks module
app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Call for Tenders API"}

@app.on_event("startup")
def startup():
    # Perform any startup logic here (e.g., connect to the database)
    pass

@app.on_event("shutdown")
def shutdown():
    # Perform any cleanup logic here (e.g., close database connections)
    engine.dispose()
