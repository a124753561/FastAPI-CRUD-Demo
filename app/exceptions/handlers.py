from fastapi import Request
from fastapi.responses import JSONResponse


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
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @app.exception_handler(ConflictException)
    async def conflict_handler(_request: Request, exc: ConflictException):
        return JSONResponse(status_code=409, content={"detail": exc.detail})

    @app.exception_handler(BadRequestException)
    async def bad_request_handler(_request: Request, exc: BadRequestException):
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @app.exception_handler(Exception)
    async def unhandled_handler(_request: Request, _exc: Exception):
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
