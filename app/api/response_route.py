import json
from typing import Any, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from app.schemas.response import ApiResponse

DEFAULT_SUCCESS_MESSAGES: dict[int, str] = {
    200: "操作成功",
    201: "创建成功",
    204: "删除成功",
}


class ApiResponseRoute(APIRoute):
    """Custom APIRoute that wraps all JSON endpoint responses in ApiResponse envelope."""

    def get_route_handler(self) -> Callable[..., Any]:
        original_route_handler = super().get_route_handler()
        default_message = self._get_default_message()

        async def wrapped_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)

            # Check if the response is JSON based on content-type or type
            content_type = response.headers.get("content-type", "")
            is_json = "application/json" in content_type or isinstance(response, JSONResponse)

            if not is_json:
                # Non-JSON response: wrap empty bodies, pass through others
                body = getattr(response, "body", b"")
                if not body:
                    return JSONResponse(
                        content=ApiResponse(
                            code=response.status_code,
                            message=default_message,
                            data=None,
                        ).model_dump(),
                        status_code=response.status_code,
                    )
                return response

            body_bytes: bytes = response.body
            try:
                parsed_body: Any = json.loads(body_bytes)
            except (json.JSONDecodeError, UnicodeDecodeError):
                return response

            # Avoid double-wrapping — exception handlers already produce ApiResponse
            if isinstance(parsed_body, dict) and "code" in parsed_body and "message" in parsed_body:
                return response

            message: str = getattr(request.state, "response_message", None) or default_message

            wrapped = ApiResponse(
                code=response.status_code,
                message=message,
                data=parsed_body,
            ).model_dump()

            return JSONResponse(content=wrapped, status_code=response.status_code)

        return wrapped_handler

    def _get_default_message(self) -> str:
        status: int = getattr(self, "status_code", None) or 200
        return DEFAULT_SUCCESS_MESSAGES.get(status, "操作成功")
