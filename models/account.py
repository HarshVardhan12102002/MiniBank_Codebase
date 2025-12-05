import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from ..database import Base

class AccountStatusEnum(enum.Enum):
    ACTIVE = "ACTIVE"
    PENDING_KYC = "PENDING_KYC"

class Account(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    status = Column(Enum(AccountStatusEnum), nullable=False, default=AccountStatusEnum.PENDING_KYC)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
