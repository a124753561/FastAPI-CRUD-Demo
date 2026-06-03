from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.response import ApiResponse


class NotFoundException(Exception):
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail


class ConflictException(Exception):
    def __init__(self, detail: str = "Resource conflict"):
        self.detail = detail


class BadRequestException(Exception):
    def __init__(self, detail: str = "Bad request"):
        self.detail = detail


def register_exception_handlers(app):
    @app.exception_handler(NotFoundException)
    async def not_found_handler(_request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=404,
            content=ApiResponse(code=404, message=exc.detail, data=None).model_dump(),
        )

    @app.exception_handler(ConflictException)
    async def conflict_handler(_request: Request, exc: ConflictException):
        return JSONResponse(
            status_code=409,
            content=ApiResponse(code=409, message=exc.detail, data=None).model_dump(),
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_handler(_request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=400,
            content=ApiResponse(code=400, message=exc.detail, data=None).model_dump(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(code=exc.status_code, message=exc.detail, data=None).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(_request: Request, _exc: Exception):
        return JSONResponse(
            status_code=500,
            content=ApiResponse(code=500, message="Internal server error", data=None).model_dump(),
        )
