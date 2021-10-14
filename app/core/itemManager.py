from datetime import datetime

from ..db.models.item import Item as ItemDBModel, ItemDescription as ItemDescriptionModel
from ..routers.models.item import Item
from .languageInfo import Language


class ItemManager:
    def __init__(self, db_handler):
        self._db_handler = db_handler

    def insert(self, item: Item, auth_name: str) -> int:
        # FIXME: 동일한 값의 이름이 있는지 확인을 한다.
        # 동일한 값의 제목이 있다면 Insert하지 않고 Error를 처리한다.

        item_db_model: ItemDBModel = ItemDBModel(
            price=item.price, registrant=auth_name, reg_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        )
        self._db_handler.insert(item_db_model)

        item_description_model: ItemDescriptionModel = ItemDescriptionModel(
            item_idx=item_db_model.idx, title=item.title, content=item.content, language=Language.KO.value
        )
        self._db_handler.insert(item_description_model)

        return item_db_model.idx