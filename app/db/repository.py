import abc

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

    def get_items_by_idx(self, idx: int):
        query = self.session.query(Item, ItemDescription).filter(Item.idx == ItemDescription.item_idx)
        if idx is not None:
            query = query.filter(Item.idx == idx)

        return query.all()

    def update(self):
        print("update")

    def get_change_history_items_by_idx(self, idx: int):
        query = self.session.query(ItemChangeHistory)
        if idx is not None:
            query = query.filter_by(item_idx=idx)

        return query.all()

    def get_item_by_title(self, title: str):
        return self.session.query(ItemDescription).filter_by(title=title).all()
