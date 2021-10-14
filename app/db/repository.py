import abc
from typing import Dict

from .models.item import Item
from datetime import datetime


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item: Item):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self):
        pass

    def insert(self):
        print("insert")

    def get(self):
        print("get")

    def update(self):
        print("update")
