from datetime import datetime

import pytest

from app.core.itemManager import ItemManager
from app.db.models.item import Item as ItemDBModel
from app.db.repository import SqlAlchemyRepository
from app.routers.models.item import Item


@pytest.fixture
def db_handler(session):
    yield SqlAlchemyRepository(session)


@pytest.fixture
def item():
    yield Item(title="Title", content="Content", price=16000)


@pytest.mark.freeze_time
def test_insert_item(db_handler, item):
    item_manager = ItemManager(db_handler)
    item_manager.insert(item, auth_name="Auth user")

    expected = [
        ItemDBModel(price=16000, registrant="Auth user", reg_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
    ]
    assert db_handler.session.query(ItemDBModel).all() == expected


@pytest.mark.freeze_time
def test_insert_duplicate_item(db_handler, item):
    item_manager = ItemManager(db_handler)
    item_manager.insert(item, auth_name="Auth user")

    expected = [
        ItemDBModel(price=16000, registrant="Auth user", reg_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
    ]
    assert db_handler.session.query(ItemDBModel).all() == expected

    with pytest.raises(Exception) as e:
        item_manager = ItemManager(db_handler)
        item_manager.insert(item, auth_name="Auth user")

    assert str(e.value) == "제목이 중복이 됩니다."

