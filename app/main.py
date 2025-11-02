# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Call for Tenders API",
    description="API to monitor and analyze EU tender calls",
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
app.include_router(tasks.router)

# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK, tags=["System"])
async def health_check():
    return {"status": "healthy"}

# Startup/shutdown events for database
@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
def shutdown_db():
    engine.dispose()

