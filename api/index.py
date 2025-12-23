# This is your FastAPI app, moved for Vercel
# ...existing code from main.py...

import sys
sys.path.append('..')  # Ensure parent dir is in path for imports if needed

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os

# Configuration from environment variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000,http://127.0.0.1:5500").split(",")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pilot_program.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PilotSignup(Base):
    __tablename__ = "pilot_signups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com"
            }
        }

class SignupResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

app = FastAPI(
    title="Cyndro Pilot Program API",
    description="API for storing pilot program signups",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Cyndro Pilot Program API", "status": "running"}

@app.post("/api/signup", response_model=SignupResponse)
def create_signup(signup: SignupRequest, db: Session = Depends(get_db)):
    existing_signup = db.query(PilotSignup).filter(PilotSignup.email == signup.email).first()
    if existing_signup:
        raise HTTPException(
            status_code=400,
            detail="This email is already registered for the pilot program"
        )
    db_signup = PilotSignup(
        name=signup.name,
        email=signup.email
    )
    db.add(db_signup)
    db.commit()
    db.refresh(db_signup)
    return db_signup

@app.get("/api/signups", response_model=list[SignupResponse])
def get_signups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    signups = db.query(PilotSignup).offset(skip).limit(limit).all()
    return signups

@app.get("/api/signups/{signup_id}", response_model=SignupResponse)
def get_signup(signup_id: int, db: Session = Depends(get_db)):
    signup = db.query(PilotSignup).filter(PilotSignup.id == signup_id).first()
    if signup is None:
        raise HTTPException(status_code=404, detail="Signup not found")
    return signup

@app.get("/health")
def health_check():
    return {"status": "healthy"}
