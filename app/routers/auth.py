import json
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from .models.item import Item

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/item")
async def item(item: Item):
    # TODO: Request 정보를 받아서 DB에 저장을 한다.
    print(item)
    return JSONResponse(status_code=status.HTTP_200_OK, content="OK")


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
