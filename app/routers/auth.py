from fastapi import APIRouter, Depends, Header

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/item")
async def item():
    return "OK"
