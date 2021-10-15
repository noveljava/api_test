from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy.orm import mapper

from .models.item import Item as ItemModel, ItemDescription as ItemDescriptionModel, \
    ItemChangeHistory as ItemChangeHistoryModel

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

item_description = Table(
    "item_description",
    metadata,
    Column("idx", Integer, unique=True, primary_key=True, index=True, autoincrement=True),
    Column("item_idx", Integer),
    Column("language", Integer),
    Column("title", String, unique=True),
    Column("content", String),
)

item_change_history = Table(
    "item_change_history",
    metadata,
    Column("idx", Integer, unique=True, primary_key=True, index=True, autoincrement=True),
    Column("item_idx", Integer),
    Column("title", String, default=None),
    Column("content", String, default=None),
    Column("price", Integer, default=None),
    Column("fee", Integer, default=None),
    Column("registrant", String),
    Column("reg_date", String)
)


def start_mappers():
    mapper(ItemModel, item)
    mapper(ItemDescriptionModel, item_description)
    mapper(ItemChangeHistoryModel, item_change_history)
