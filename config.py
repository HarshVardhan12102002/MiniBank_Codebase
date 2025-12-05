
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./minibank.db")
    UIDAI_MOCK_URL: str = os.getenv("UIDAI_MOCK_URL", "http://localhost:9001")
    PAN_MOCK_URL: str = os.getenv("PAN_MOCK_URL", "http://localhost:9002")
    EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "localhost")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", 1025))
    S3_BUCKET: str = os.getenv("S3_BUCKET", "mock-bucket")
    BANK_CODE: str = os.getenv("BANK_CODE", "1023")
    BRANCH_CODE: str = os.getenv("BRANCH_CODE", "001")
    SEQUENCE_START: int = int(os.getenv("SEQUENCE_START", 10000000))

settings = Settings()
