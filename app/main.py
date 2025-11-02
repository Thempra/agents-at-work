# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, get_db
from app.routers.tasks import router as tasks_router

app = FastAPI(
    title="Call for Tenders API",
    description="API para monitoreo y análisis de convocatorias de la UE",
    version="1.0.0",
)

origins = ["*"]  # Permisiva para desarrollo, modificar según sea necesario

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de Call for Tenders"}

