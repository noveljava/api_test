from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from .models.item import Item, ItemChange
from ..core.itemManager import ItemManager
from ..db.repository import SqlAlchemyRepository
from ..db.session import get_session
from loguru import logger

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/item")
async def item(req_item: Item, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    try:
        idx = ItemManager(db_handler).insert(req_item, "Auth_User")
        response = {"idx": idx}
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    except Exception as e:
        logger.error(f"ERROR: Item 등록 중 에러가 발생했습니다.\n {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"err_msg": "서버에 문제가 발생했습니다."})


@router.get("/item")
@router.get("/item/{idx}")
async def item(idx: int = None, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    query_result = ItemManager(db_handler).get_items_by_idx(idx)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"items": query_result})


@router.put("/item/{idx}")
async def item(idx: int, item_change: ItemChange, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)

    try:
        idx = ItemManager(db_handler).insert_change_history(idx, item_change, "Auth_User")
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"err_msg": str(e)})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"idx": idx})


@router.get("/change-history/item/{idx}")
async def item(idx: int = None, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    query_result = ItemManager(db_handler).get_change_history_items_by_idx(idx)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"items": query_result})
