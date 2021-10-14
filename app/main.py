import uvicorn
from fastapi import FastAPI
from loguru import logger
from sqlalchemy.orm import clear_mappers

from .routers import auth
from .db.orm import start_mappers
from .db.session import make_engine, make_all_table

app = FastAPI(
    title="API Test",
    description="API Test.",
    version="1.0.0",
)

app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    make_engine()
    start_mappers()
    make_all_table()
    logger.add("./log/server_{time}.log", level="ERROR", rotation="500 MB")


@app.on_event("shutdown")
async def shutdown_event():
    clear_mappers()


def run():
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)


if __name__ == "__main__":
    run()
