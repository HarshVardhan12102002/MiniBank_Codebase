import uuid
from sqlalchemy import Column, String, Integer, DateTime, func
from ..database import Base

class EmailAudit(Base):
    __tablename__ = "email_audit"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    email_type = Column(String, nullable=False)
    template_version = Column(String, nullable=True)
    send_status = Column(String, nullable=False)
    attempts = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AadhaarAttempt(Base):
    __tablename__ = "aadhaar_attempts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=True, index=True)
    aadhaar_number_masked = Column(String, nullable=True)
    attempts = Column(Integer, default=0)
    blocked_until = Column(DateTime, nullable=True)
    last_attempted_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
