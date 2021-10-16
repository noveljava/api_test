from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from ..core.itemManager import ItemManager
from ..db.repository import SqlAlchemyRepository
from ..db.session import get_session
from ..core.languageInfo import Language

router = APIRouter(prefix="/customer", tags=["customer"])


@router.get("/item")
@router.get("/item/{idx}")
async def item(idx: int = None, lang: str = None, session=Depends(get_session)):
    if lang is None or lang.lower() not in ['ko', 'en', 'ch']:
        lang = 'ko'

    db_handler = SqlAlchemyRepository(session)
    query_result = ItemManager(db_handler).get_items_by_idx(idx, "N", lang)

    # 환율 정보는 변경이 되어야한다.
    exchange_rate = {
        Language.KO.name.lower(): 1,
        Language.EN.name.lower(): 1.2,
        Language.CH.name.lower(): 1.6
    }

    for v in query_result:
        v['price'] *= exchange_rate[lang]

    return JSONResponse(status_code=status.HTTP_200_OK, content={"items": query_result})
