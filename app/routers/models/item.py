from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    title: Optional[str]
    content: Optional[str]
    price: Optional[int]

    # Optional
    fee: Optional[int]


class ItemChange(BaseModel):
    # Optional
    title: Optional[str]
    content: Optional[str]
    price: Optional[int]
    fee: Optional[int]
