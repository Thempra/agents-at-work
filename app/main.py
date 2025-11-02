# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Call for Tenders API",
    description="API for managing Call for Tenders data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Permissive CORS configuration
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

@app.get("/", tags=["health"])
def read_root():
    return {"message": "Call for Tenders API is running"}

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.on_event("startup")
async def startup():
    # Perform any startup tasks here
    pass

@app.on_event("shutdown")
async def shutdown():
    # Perform any cleanup tasks here
    pass
