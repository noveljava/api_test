from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from typing import Optional

from .models.item import Item, ItemChange
from ..core.itemManager import ItemManager
from ..db.repository import SqlAlchemyRepository
from ..db.session import get_session
from loguru import logger

router = APIRouter(prefix="/editor", tags=["editor"])


@router.get("/item")
@router.get("/item/{idx}")
async def item(idx: int = None, wait: str = None, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    query_result = ItemManager(db_handler).get_items_by_idx(idx, wait)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"items": query_result})


@router.put("/item/{idx}")
async def item(idx: int, item: Item, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    ItemManager(db_handler).update_item(idx, item, "Editor")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"idx": idx})

