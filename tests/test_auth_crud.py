from datetime import datetime

import pytest

from app.core.itemManager import ItemManager
from app.db.models.item import Item as ItemDBModel
from app.db.repository import SqlAlchemyRepository
from app.routers.models.item import Item


@pytest.fixture
def db_handler(session):
    yield SqlAlchemyRepository(session)


@pytest.mark.freeze_time
def test_valid_signup(db_handler):
    item: Item = Item(title="Title", content="Content", price=16000)

    item_manager = ItemManager(db_handler)
    item_manager.insert(item, auth_name="Auth user")

    expected = [
        ItemDBModel(price=16000, registrant="Auth user", reg_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")),
    ]
    #
    assert db_handler.session.query(ItemDBModel).all() == expected
