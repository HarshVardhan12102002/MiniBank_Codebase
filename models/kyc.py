import uuid
from sqlalchemy import Column, String, DateTime, func, Enum
from ..database import Base

class KYCDocument(Base):
    __tablename__ = "kyc_documents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False, index=True)
    document_type = Column(String, nullable=False)
    s3_url = Column(String, nullable=False)
    object_key = Column(String, nullable=False)
    mime_type = Column(String, nullable=True)
    file_size = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
