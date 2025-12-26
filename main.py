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
# Set ALLOWED_ORIGINS in production, e.g., "https://cyndro.com,https://www.cyndro.com"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000,http://127.0.0.1:5500").split(",")


# Database setup
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Database Model
class PilotSignup(Base):
    __tablename__ = "pilot_signups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)


# Pydantic schemas
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


# FastAPI app
app = FastAPI(
    title="Cyndro Pilot Program API",
    description="API for storing pilot program signups",
    version="1.0.0"
)

# CORS middleware - allow requests from your frontend
# Configure allowed origins via ALLOWED_ORIGINS environment variable in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# Dependency to get DB session
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
    """
    Create a new pilot program signup
    """
    # Check if email already exists
    existing_signup = db.query(PilotSignup).filter(PilotSignup.email == signup.email).first()
    if existing_signup:
        raise HTTPException(
            status_code=400,
            detail="This email is already registered for the pilot program"
        )
    
    # Create new signup
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
    """
    Get all pilot program signups (for admin purposes)
    """
    signups = db.query(PilotSignup).offset(skip).limit(limit).all()
    return signups


@app.get("/api/signups/{signup_id}", response_model=SignupResponse)
def get_signup(signup_id: int, db: Session = Depends(get_db)):
    """
    Get a specific signup by ID
    """
    signup = db.query(PilotSignup).filter(PilotSignup.id == signup_id).first()
    if signup is None:
        raise HTTPException(status_code=404, detail="Signup not found")
    return signup


@app.get("/health")
def health_check():
    return {"status": "healthy"}

