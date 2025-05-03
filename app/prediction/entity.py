from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    probability = Column(Float, nullable=False)
    prediction = Column(String, nullable=False)
    
    # Relationship with the User model
    user = relationship("User", back_populates="predictions")