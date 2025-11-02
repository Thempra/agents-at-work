# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks

app = FastAPI(
    title="Call for Tenders",
    description="API para el monitoreo y análisis de convocatorias de la Unión Europea",
    version="1.0.0",
    contact={
        "name": "Tu Nombre",
        "url": "https://github.com/tu-usuario/call-for-tenders"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

app.include_router(tasks.router)
