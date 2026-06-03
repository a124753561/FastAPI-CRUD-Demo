from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.config import settings
from app.database import Base, engine
from app.exceptions.handlers import register_exception_handlers
from app.schemas.response import ApiResponse


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    register_exception_handlers(app)

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_request: Request, exc: RequestValidationError):
        errors = exc.errors()
        detail = "; ".join(f"{e['loc'][-1]}: {e['msg']}" for e in errors)
        return JSONResponse(
            status_code=422,
            content=ApiResponse(code=422, message=detail, data=None).model_dump(),
        )

    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT)
