from jose import JWTError, jwt
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import settings
from app.schemas.response import ApiResponse

AUTH_WHITELIST: set[tuple[str, str]] = {
    ("POST", "/api/v1/auth/login"),
    ("POST", "/api/v1/auth/refresh"),
    ("POST", "/api/v1/users/"),
}

DOCS_PREFIXES = ("/docs", "/redoc", "/openapi.json")


class AuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        path = request.url.path
        method = request.method

        if (method, path) in AUTH_WHITELIST or path.startswith(DOCS_PREFIXES):
            await self.app(scope, receive, send)
            return

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            response = JSONResponse(
                status_code=401,
                content=ApiResponse(code=401, message="未登录或 token 已过期", data=None).model_dump(),
            )
            await response(scope, receive, send)
            return

        token = auth_header.removeprefix("Bearer ")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("type") != "access":
                raise JWTError("invalid token type")
            user_id = payload.get("user_id")
            if user_id is None:
                raise JWTError("missing user_id")
        except JWTError:
            response = JSONResponse(
                status_code=401,
                content=ApiResponse(code=401, message="无效的认证凭证", data=None).model_dump(),
            )
            await response(scope, receive, send)
            return

        request.state.user_id = user_id
        scope["user_id"] = user_id
        await self.app(scope, receive, send)
