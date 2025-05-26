from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp_code = Column(String, nullable=False)
    expired_time = Column(BigInteger, nullable=False)  # UNIX timestamp
    otp_used = Column(Boolean, default=False)
    
    # Relationship to User
    user = relationship("User", back_populates="otps")