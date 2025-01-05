from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, Message, User, SessionLocal, engine
from pydantic import BaseModel
from sqlalchemy.exc import OperationalError, IntegrityError
from time import sleep
import logging
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust the origin to match your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log request details
    start_time = time.time()
    logging.info(f"New request: {request.method} {request.url.path}")
    
    response = await call_next(request)  # Process the request
    
    # Log response details
    process_time = time.time() - start_time
    logging.info(f"Completed request: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    return response

# Define data models for Pydantic validation
class MessageBase(BaseModel):
    user_id: int
    content: str

class UserBase(BaseModel):
    username: str
    email: str

# Dependency to get database session
def get_db():
    retries = 5
    db = None
    for attempt in range(retries):
        try:
            db = SessionLocal()
            yield db
            break
        except OperationalError as e:
            logging.error(f"Database connection failed, retrying... {attempt + 1}/{retries}")
            sleep(2)
        finally:
            if db:
                db.close()

# Routes
@app.post("/messages/", response_model=MessageBase)
async def create_message(message: MessageBase, db: Session = Depends(get_db)):
    db_message = Message(user_id=message.user_id, content=message.content)
    db.add(db_message)
    db.commit()
    return db_message

@app.get("/messages/")
def read_messages(db: Session = Depends(get_db)):
    return db.query(Message).all()

@app.post("/users/", response_model=UserBase)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    logging.info(f"Attempting to create user with email: {user.email}")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logging.warning(f"Duplicate email found: {user.email}")
        raise HTTPException(
            status_code=400,
            detail=f"User with email {user.email} already exists."
        )
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
