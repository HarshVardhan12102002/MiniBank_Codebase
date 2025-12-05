from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from .config import settings

connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

def init_db():
    # import models here so metadata is available
    from .models.customer import Customer
    from .models.account import Account
    from .models.aadhaar_attempt import AadhaarAttempt
    Base.metadata.create_all(bind=engine)
