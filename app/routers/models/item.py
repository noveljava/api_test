from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    content: str
    price: int

    # Optional
    fee: Optional[int]


class ItemChange(BaseModel):
    # Optional
    title: Optional[str]
    content: Optional[str]
    price: Optional[int]
    fee: Optional[int]
