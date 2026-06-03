import contextvars
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor

from app.database import SessionLocal
from app.models.request_log import RequestLog
from app.schemas.response import trace_id_ctx

MAX_BODY_LENGTH = 4096
MAX_RESPONSE_PRINT_LENGTH = 64
MASK_VALUE = "******"

SENSITIVE_HEADERS = {"authorization", "cookie", "x-api-key"}
SENSITIVE_BODY_FIELDS = {"password", "password_confirm", "old_password", "new_password", "secret", "token"}

_log_executor = ThreadPoolExecutor(max_workers=4)
_logger = logging.getLogger("request")


def mask_headers(headers: dict) -> str:
    masked = {}
    for key, value in headers.items():
        lower = key.lower()
        if lower == "authorization" and value:
            parts = value.split(" ", 1)
            masked[key] = f"{parts[0]} {MASK_VALUE}" if len(parts) > 1 else MASK_VALUE
        elif lower in SENSITIVE_HEADERS:
            masked[key] = MASK_VALUE
        else:
            masked[key] = value
    return json.dumps(masked, ensure_ascii=False)


def mask_body(body_str: str) -> str:
    if not body_str:
        return body_str
    try:
        data = json.loads(body_str)
        _mask_json(data)
        return json.dumps(data, ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        return body_str


def _mask_json(data):
    if isinstance(data, dict):
        for key in list(data.keys()):
            if key.lower() in SENSITIVE_BODY_FIELDS:
                data[key] = MASK_VALUE
            else:
                _mask_json(data[key])
    elif isinstance(data, list):
        for item in data:
            _mask_json(item)


def _write_log(log_data: dict) -> None:
    session = SessionLocal()
    try:
        entry = RequestLog(**log_data)
        session.add(entry)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


class RequestLoggingMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.monotonic()

        # Read metadata from scope (no receive consumption)
        method = scope["method"]

        # Build full URL from scope
        scheme = scope.get("scheme", "http")
        server = scope.get("server", ("unknown", 80))
        host = server[0] if server else "unknown"
        port = server[1] if server else 80
        path = scope["path"]
        query_string = scope.get("query_string", b"").decode()
        url = f"{scheme}://{host}:{port}{path}"
        if query_string:
            url += f"?{query_string}"

        client = scope.get("client")
        client_ip = client[0] if client else None

        # Collect headers from scope
        headers: dict[str, str] = {}
        user_agent = ""
        for key, value in scope.get("headers", []):
            name = key.decode("latin-1").lower()
            val = value.decode("latin-1")
            headers[name] = val
            if name == "user-agent":
                user_agent = val

        # Wrap receive to capture request body WITHOUT consuming it
        body_chunks: list[bytes] = []

        async def capture_receive():
            message = await receive()
            if message["type"] == "http.request":
                chunk = message.get("body", b"")
                if chunk:
                    body_chunks.append(chunk)
            return message

        # Wrap send to capture response body
        response_chunks: list[bytes] = []
        response_status = 0

        async def capture_send(message):
            nonlocal response_status
            if message["type"] == "http.response.start":
                response_status = message["status"]
            elif message["type"] == "http.response.body":
                chunk = message.get("body", b"")
                if chunk:
                    response_chunks.append(chunk)
            await send(message)

        await self.app(scope, capture_receive, capture_send)

        response_time_ms = round((time.monotonic() - start) * 1000)
        request_body_bytes = b"".join(body_chunks) if body_chunks else None
        response_body_bytes = b"".join(response_chunks)
        response_body_str = response_body_bytes.decode("utf-8", errors="replace")

        log_data = {
            "trace_id": trace_id_ctx.get(),
            "url": url,
            "method": method,
            "query_params": query_string if query_string else None,
            "request_body": mask_body(request_body_bytes.decode("utf-8", errors="replace")) if request_body_bytes else None,
            "response_body": response_body_str[:MAX_BODY_LENGTH] if response_body_str else None,
            "status_code": response_status,
            "response_time_ms": response_time_ms,
            "client_ip": client_ip,
            "user_agent": user_agent[:512] if user_agent else None,
            "request_headers": mask_headers(headers),
            "user_id": scope.get("user_id"),
        }

        ctx = contextvars.copy_context()
        _log_executor.submit(ctx.run, _write_log, log_data)
        body_preview = response_body_str[:MAX_RESPONSE_PRINT_LENGTH] if response_body_str else ""
        _logger.info("%s %s → %d (%dms) %s", method, url, response_status, response_time_ms, body_preview)
