from dataclasses import asdict
from datetime import datetime
from typing import List

from .languageInfo import Language
from .languageInfo import Language
from ..db.models.item import Item as ItemDBModel, ItemDescription as ItemDescriptionModel
from ..routers.models.item import Item


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

    def get_items_by_idx(self, idx: int) -> List:
        result = []
        tmp_dict = {}
        for e in self._db_handler.get_items_by_idx(idx):
            if e[0].idx not in tmp_dict.keys():
                tmp_dict[e[0].idx] = asdict(e[0])

            item_description = asdict(e[1])
            lang = Language(item_description['language']).name
            tmp_dict[item_description['item_idx']][lang] = item_description

        for e in tmp_dict.values():
            result.append(e)

        return result
