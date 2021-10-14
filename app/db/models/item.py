from dataclasses import dataclass
from typing import Optional


@dataclass(unsafe_hash=True)
class Item:
    idx: int
    price: int
    registrant: str
    reg_date: str

    # Optional Data
    age: Optional[int] = None
    confirmed_editor: Optional[str] = None
    update_date: Optional[str] = None

