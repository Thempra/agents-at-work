# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks

app = FastAPI(
    title="Call for Tenders API",
    version="1.0.0",
    description="RESTful API for managing calls for tenders"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(tasks.router)
