from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base

class AadhaarAttempt(Base):
    __tablename__ = "aadhaar_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=True, index=True)
    aadhaar_masked = Column(String(12), nullable=True, index=True)
    attempts = Column(Integer, default=0)
    blocked_until = Column(DateTime, nullable=True)
    last_attempted_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
