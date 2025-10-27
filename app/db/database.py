from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


engine = create_engine(settings.database_url)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

