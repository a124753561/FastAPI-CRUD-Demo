import logging
import uuid

from starlette.requests import Request

from app.config import settings
from app.schemas.response import trace_id_ctx


class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_ctx.get()
        return True


def setup_logging() -> None:
    fmt = "%(asctime)s [%(levelname)s] [%(trace_id)s] %(name)s: %(message)s"
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S"))
    handler.addFilter(TraceIdFilter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

    if settings.DEBUG:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").propagate = False


class TraceIdMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        token = trace_id_ctx.set(uuid.uuid4().hex)
        try:
            await self.app(scope, receive, send)
        finally:
            trace_id_ctx.reset(token)
