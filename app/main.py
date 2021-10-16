import uvicorn
from fastapi import FastAPI
from loguru import logger
from sqlalchemy.orm import clear_mappers
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from .routers import auth, editor
from .db.orm import start_mappers
from .db.session import make_engine, make_all_table

app = FastAPI(
    title="API Test",
    description="API Test.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(editor.router)


@app.on_event("startup")
async def startup_event():
    make_engine()
    start_mappers()
    make_all_table()
    logger.add("./log/server_{time}.log", level="ERROR", rotation="500 MB")


@app.on_event("shutdown")
async def shutdown_event():
    clear_mappers()


# entity Error가 났을 시에 402로 처리되는 부분을 500 으로 고정.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=500)


def run():
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
    run()
