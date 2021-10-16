from dataclasses import asdict
from typing import List
from ..utils.utils import get_current_time
from .languageInfo import Language
from ..db.models.item import Item as ItemDBModel, ItemDescription as ItemDescriptionModel, \
    ItemChangeHistory as ItemChangeHistoryModel
from ..routers.models.item import Item, ItemChange


class ItemManager:
    def __init__(self, db_handler):
        self._db_handler = db_handler

    def insert(self, item: Item, auth_name: str) -> int:
        required = ["title", "content", "price"]
        for v in required:
            if item.dict()[v] is None:
                raise Exception("필수적인 요소가 다 들어오지 않았습니다.")

        if len(self._db_handler.get_item_by_title(item.title)) != 0:
            raise Exception("제목이 중복이 됩니다.")

        item_db_model: ItemDBModel = ItemDBModel(
            price=item.price, registrant=auth_name, reg_date=get_current_time()
        )
        self._db_handler.insert(item_db_model)

        item_description_model: ItemDescriptionModel = ItemDescriptionModel(
            item_idx=item_db_model.idx, title=item.title, content=item.content, language=Language.KO.value
        )
        self._db_handler.insert(item_description_model)

        return item_db_model.idx

    def get_items_by_idx(self, idx: int, wait: str = None) -> List:
        result = []
        tmp_dict = {}
        for e in self._db_handler.get_items_by_idx(idx, wait):
            if e[0].idx not in tmp_dict.keys():
                tmp_dict[e[0].idx] = asdict(e[0])

            item_description = asdict(e[1])
            lang = Language(item_description['language']).name
            tmp_dict[item_description['item_idx']][lang] = item_description

        for e in tmp_dict.values():
            result.append(e)

        return result

    def _is_exist(self, idx):
        return len(self.get_items_by_idx(idx)) != 0

    def insert_change_history(self, idx: int, item_change: ItemChange, auth_name: str) -> int:
        if not self._is_exist(idx):
            raise Exception("해당 아이템을 찾을 수 없습니다.")

        item_change_history: ItemChangeHistoryModel = ItemChangeHistoryModel(
            item_idx=idx, registrant=auth_name, reg_date=get_current_time()
        )

        item_change_history.assign(item_change)
        self._db_handler.insert(item_change_history)

        return item_change_history.idx

    def get_change_history_items_by_idx(self, idx: int) -> List:
        return [asdict(e) for e in self._db_handler.get_change_history_items_by_idx(idx)]

    def update_item(self, idx: int, item: Item, editor_name: str):
        if not self._is_exist(idx):
            raise Exception("해당 아이템을 찾을 수 없습니다.")

        item_update_content = {'updater': editor_name, 'update_date': get_current_time()}
        item_description_update_content = {}

        item_element = ['price', 'fee']
        item_description = ['title', 'content']

        for k, v in item.dict().items():
            if v is None:
                continue

            if k in item_element:
                item_update_content[k] = v
            elif k in item_description:
                item_description_update_content[k] = v

        self._db_handler.update_item(idx, item_update_content)
        if len(item_description_update_content) != 0:
            self._db_handler.update_item_description(idx, item_description_update_content)
