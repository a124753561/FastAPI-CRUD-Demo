from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_v1_router
from app.config import settings
from app.database import Base, engine
from app.exceptions.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
    register_exception_handlers(app)
    return app


app = create_app()
