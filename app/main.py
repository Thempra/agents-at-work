# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Security, BackgroundTasks, Request, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import tasks
from app.schemas import CallCre

app = FastAPI(
    title="Call for Tenders API",
    description="API for managing tenders and convocatorias from the European Union.",
    version="1.0.0",
)

# CORS Configuration (permissive for development)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root(request: Request):
    return {"message": "Welcome to the Call for Tenders API", "url": request.url}

@app.get("/healthcheck", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    try:
        # Check if we can connect to the database
        db.execute("SELECT 1")
        return {"status": "healthy"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Database is not healthy")

@app.on_event("shutdown")
async def shutdown_event():
    # Perform any cleanup tasks here if needed
    pass

# Include other routers and dependencies as needed
