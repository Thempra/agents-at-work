# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks

app = FastAPI(
    title="Call for Tenders",
    description="API for managing and analyzing Call for Tenders data.",
    version="1.0.0"
)

# CORS configuration (permissive for development)
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization (create tables)
Base.metadata.create_all(bind=engine)

# Router imports from app.routers.tasks
from app.routers import tasks

app.include_router(tasks.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Call for Tenders API"}

@app.on_event("startup")
async def startup_event():
    # Startup event logic here (e.g., database connection)
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown event logic here (e.g., closing database connections)
    pass
