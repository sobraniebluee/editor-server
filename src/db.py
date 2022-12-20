import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from src.config import DBConfig


engine = create_engine(DBConfig.DB_URL_CONNECT, echo=False)
session_factory = sessionmaker(engine, autoflush=False)
session = scoped_session(session_factory)
Base = declarative_base()
Base.query = session.query_property()


def create_metadata():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        exit(f"Error connect to database and create metadata!\n "
             f"Detail error: {e}")
