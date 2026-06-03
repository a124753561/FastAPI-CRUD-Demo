import contextvars
from datetime import datetime, timezone
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")

trace_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default="")


class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: str = Field(default_factory=lambda: trace_id_ctx.get())
