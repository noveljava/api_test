
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./item_info.db"
engine = None
SessionLocal: sessionmaker
Base = declarative_base()


def make_engine(sqlalchemy_database_url = None):
    global SessionLocal, engine, SQLALCHEMY_DATABASE_URL
    engine_url = SQLALCHEMY_DATABASE_URL
    if sqlalchemy_database_url is not None:
        engine_url = sqlalchemy_database_url

    engine = create_engine(
        engine_url, connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    global SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def make_all_table():
    from .orm import metadata
    metadata.create_all(bind=engine)
