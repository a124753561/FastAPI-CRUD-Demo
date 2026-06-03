from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.config import settings
from app.database import Base, engine
from app.exceptions.handlers import register_exception_handlers
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.trace import TraceIdMiddleware, setup_logging
from app.schemas.response import ApiResponse


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(TraceIdMiddleware)
    register_exception_handlers(app)

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_request: Request, exc: RequestValidationError):
        errors = exc.errors()
        parts = []
        for e in errors:
            msg = e["msg"].removeprefix("Value error, ")
            meaningful = [p for p in e["loc"] if p != "body"]
            if meaningful:
                loc_str = " -> ".join(str(p) for p in meaningful)
                parts.append(f"{loc_str}: {msg}")
            else:
                parts.append(msg)
        return JSONResponse(
            status_code=422,
            content=ApiResponse(code=422, message="; ".join(parts), data=None).model_dump(),
        )

    app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=settings.PORT, access_log=False)
