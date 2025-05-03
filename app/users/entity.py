from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)  # Added unique constraint
    email = Column(String, unique=True, nullable=False)
    phonenumber = Column(String, nullable=True, unique=True)  # Added unique constraint
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String, nullable=False, default="user")  # Added role field with default value