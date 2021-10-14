from dataclasses import dataclass
from typing import Optional


@dataclass(unsafe_hash=True)
class Item:
    price: int
    registrant: str
    reg_date: str

    # Optional Data
    idx: Optional[int] = None
    age: Optional[int] = None
    confirmed_editor: Optional[str] = None
    update_date: Optional[str] = None


@dataclass(unsafe_hash=True)
class ItemDescription:
    item_idx: int
    language: int
    title: str
    content: str

    # Optional Data
    idx: Optional[int] = None
