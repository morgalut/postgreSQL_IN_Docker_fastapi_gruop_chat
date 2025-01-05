from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://postgres:yourpassword@postgres1:5432/postgres"
print("Connecting to database at:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Message(Base):
    __tablename__ = "message"
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now())

    user = relationship("User", backref="messages")

# Check if the tables already exist before creating them
if not inspect(engine).has_table("user") and not inspect(engine).has_table("message"):
    Base.metadata.create_all(bind=engine)
