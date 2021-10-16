from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from .models.item import Item
from ..core.itemManager import ItemManager
from ..db.repository import SqlAlchemyRepository
from ..db.session import get_session

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


@router.put("/item/confirmed/{idx}")
async def item(idx: int, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    ItemManager(db_handler).confirmed(idx, "Editor")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"idx": idx})


@router.get("/change-request/item/")
@router.get("/change-request/item/{idx}")
async def changed_request_item(idx: int = None, wait: str = None, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    query_result = ItemManager(db_handler).get_change_history_items_by_item_idx(idx, wait)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"items": query_result})


@router.get("/change-request/{idx}")
async def changed_request_item(idx: int = None, wait: str = None, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    query_result = ItemManager(db_handler).get_change_history_items_by_idx(idx, wait)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"items": query_result})


@router.put("/change-request/{idx}")
async def changed_request_item(idx: int = None, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    try:
        query_result = ItemManager(db_handler).confirm_changed_history(idx, "Confirmed")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"err_msg": str(e)})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "ok"})
