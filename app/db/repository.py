import abc
from typing import Dict

from .models.item import Item, ItemDescription
from datetime import datetime


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

    def get_items_by_idx(self, idx: int):
        query = self.session.query(Item, ItemDescription).filter(Item.idx == ItemDescription.item_idx)
        if idx != 0:
            query = query.filter(Item.idx==idx)

        return query.all()

    def update(self):
        print("update")
