from sqlalchemy import Column, Integer, String, Date, DateTime, func
from ..database import Base

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    mobile = Column(String(10), unique=True, nullable=False)
    aadhaar = Column(String(12), nullable=True)
    pan = Column(String(10), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
