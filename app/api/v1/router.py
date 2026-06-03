from fastapi import APIRouter

from app.api.response_route import ApiResponseRoute
from app.api.v1.users import router as users_router

api_v1_router = APIRouter(route_class=ApiResponseRoute)
api_v1_router.include_router(users_router)
