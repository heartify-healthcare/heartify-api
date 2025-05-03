from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://cardiovasculardisease:cardiovasculardisease@localhost:5432/cardiovasculardisease")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db_connection():
    return SessionLocal()