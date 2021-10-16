import abc

from typing import Dict
from .models.item import Item, ItemDescription, ItemChangeHistory


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def insert(self, item: Item):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def insert(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get_items_by_idx(self, idx: int, wait: str = None):
        query = self.session.query(Item, ItemDescription).filter(Item.idx == ItemDescription.item_idx)
        if idx is not None:
            query = query.filter(Item.idx == idx)

        if wait is not None:
            if wait == 'y':
                query = query.filter(Item.confirmed_editor.__eq__(None))
            else:
                query = query.filter(Item.confirmed_editor.isnot(None))

        return query.all()

    def update_item(self, idx: int, update_content: Dict):
        self.session.query(Item).filter_by(idx=idx).update(update_content)
        self.session.commit()

    def update_item_description(self, idx: int, update_content: Dict):
        self.session.query(ItemDescription).filter_by(idx=idx).update(update_content)
        self.session.commit()

    def get_change_history_items_by_idx(self, idx: int, wait: str = None):
        query = self.session.query(ItemChangeHistory)
        if idx is not None:
            query = query.filter_by(item_idx=idx)

        if wait is not None:
            if wait == 'y':
                query = query.filter(confirmed_editor.__eq__(None))
            else:
                query = query.filter(confirmed_editor.isnot(None))

        return query.all()

    def get_item_by_title(self, title: str):
        return self.session.query(ItemDescription).filter_by(title=title).all()
