from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
import os

# Define data models for Pydantic validation
class Message(BaseModel):
    user_id: int
    content: str

class User(BaseModel):
    username: str
    email: str

# Initialize FastAPI app
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Database URL (adjust username, password, and ports as necessary)
DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5433/postgres"

# Initialize the database
database = Database(DATABASE_URL)

# Startup and shutdown events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Routes
@app.post("/messages/")
async def create_message(message: Message):
    query = "INSERT INTO message(user_id, content) VALUES (:user_id, :content)"
    await database.execute(query, values={"user_id": message.user_id, "content": message.content})
    return {"message": "Message sent successfully"}

@app.get("/messages/")
async def read_messages():
    query = "SELECT * FROM message"
    messages = await database.fetch_all(query)
    return messages

@app.post("/users/")
async def create_user(user: User):
    # Properly quote the table name "user" to avoid syntax errors with reserved keywords
    query = "INSERT INTO \"user\"(username, email) VALUES (:username, :email)"
    await database.execute(query, values={"username": user.username, "email": user.email})
    return {"message": "User created successfully"}

@app.get("/users/")
async def read_users():
    # Properly quote the table name "user"
    query = "SELECT * FROM \"user\""
    users = await database.fetch_all(query)
    return users
