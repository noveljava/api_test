from dataclasses import dataclass
from typing import Optional


@dataclass(unsafe_hash=True)
class Item:
    price: int
    registrant: str
    reg_date: str

    # Optional Data
    idx: Optional[int] = None
    fee: Optional[int] = None
    confirmed_editor: Optional[str] = None
    updater: Optional[str] = None
    update_date: Optional[str] = None

    def __eq__(self, other):
        keys = ["price", "registrant", "reg_date", "fee", "confirmed_editor", "update_date"]
        for key in keys:
            if self.__dict__[key] != other.__dict__[key]:
                return False

        return True


@dataclass(unsafe_hash=True)
class ItemDescription:
    item_idx: int
    language: int
    title: str
    content: str

    # Optional Data
    idx: Optional[int] = None


@dataclass(unsafe_hash=True)
class ItemChangeHistory:
    item_idx: int
    registrant: str
    reg_date: str

    # Optional Data
    idx: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    price: Optional[int] = None
    fee: Optional[int] = None
    confirmed_editor: Optional[str] = None
    confirmed_date: Optional[str] = None

    def assign(self, other):
        keys = ['title', 'content', 'price']
        for key in keys:
            if key in other.__dict__:
                self.__dict__[key] = other.__dict__[key]
