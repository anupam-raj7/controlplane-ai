"""
Database engine, session factory, and the FastAPI dependency used to get a DB session
inside route handlers.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session and always closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
