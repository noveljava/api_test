import json
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from .models.item import Item
from ..core.itemManager import ItemManager
from ..db.repository import SqlAlchemyRepository
from ..db.session import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/item")
async def item(req_item: Item, session=Depends(get_session)):
    db_handler = SqlAlchemyRepository(session)
    idx = ItemManager(db_handler).insert(req_item, "Auth_User")
    response = {"idx": idx}
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.get("/item")
@router.get("/item/{idx}")
async def item(idx: int = 0):
    # TODO : DB에 있는 친구를 가져와서 Return 시킨다.
    # idx가 없을 경우에는 모든 정보를 가져온다.

    return f"OK - {idx}"


@router.put("/item/{idx}")
async def item(idx: int):
    # TODO : idx에 대한 정보가 있는지 확인을 하고,
    # 있다면 change history에 값을 집어넣는다.
    return "OK"
