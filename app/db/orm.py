from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import mapper

from .models.item import Item as ItemModel

metadata = MetaData()

item = Table(
    "item",
    metadata,
    Column("idx", Integer, unique=True, primary_key=True, index=True, autoincrement=True),
    Column("price", Integer),
    Column("registrant", String),
    Column("fee", Integer, default=None),
    Column("confirmed_editor", String, default=None),
    Column("update_date", String, default=None),
    Column("reg_date", String)
)


def start_mappers():
    mapper(ItemModel, item)
