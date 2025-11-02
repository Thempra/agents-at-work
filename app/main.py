# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks

app = FastAPI(
    title="Call for Tenders API",
    version="1.0.0",
    description="API for managing calls for tenders",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create tables
Base.metadata.create_all(bind=engine)

# Import routers
from app.routers import tasks

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

@app.on_event("startup")
async def startup():
    db = next(get_db())
    try:
        # Perform any startup activities here
        pass
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown():
    db = next(get_db())
    try:
        # Perform any shutdown activities here
        pass
    finally:
        db.close()

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
