import pytest

from app.core.itemManager import ItemManager
from app.db.models.item import Item as ItemDBModel
from app.db.repository import SqlAlchemyRepository
from app.routers.models.item import Item


@pytest.fixture
def db_handler(session):
    yield SqlAlchemyRepository(session)


def test_valid_signup(db_handler):
    item: Item = Item(title="Title", content="Content", price=16000)

    item_manager = ItemManager(db_handler)
    item_manager.insert(item, auth_name="Auth user")

    print(db_handler.session.query(ItemDBModel).all())
    # expected = [
    #     ItemDBModel(id=valid_id, password=password, name="Test User"),
    # ]
    #
    # assert db_handler.session.query(User).all() == expected
