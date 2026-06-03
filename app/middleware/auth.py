from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
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


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        if (method, path) in AUTH_WHITELIST or path.startswith(DOCS_PREFIXES):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content=ApiResponse(code=401, message="未登录或 token 已过期", data=None).model_dump(),
            )

        token = auth_header.removeprefix("Bearer ")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("type") != "access":
                raise JWTError("invalid token type")
            user_id = payload.get("user_id")
            if user_id is None:
                raise JWTError("missing user_id")
        except JWTError:
            return JSONResponse(
                status_code=401,
                content=ApiResponse(code=401, message="无效的认证凭证", data=None).model_dump(),
            )

        request.state.user_id = user_id
        return await call_next(request)
