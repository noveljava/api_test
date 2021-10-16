import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.db.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def app():
    from app.db.session import make_all_table, make_engine
    from app.main import app
    from fastapi.testclient import TestClient

    make_engine("sqlite:///:memory:")
    start_mappers()
    make_all_table()
    yield TestClient(app)
    clear_mappers()
