from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.response_route import ApiResponseRoute
from app.database import get_db
from app.exceptions.handlers import UnauthorizedException
from app.schemas.user import LoginRequest, RefreshRequest, TokenResponse
from app.services import user as user_service
from app.services.auth import create_access_token, create_refresh_token, get_user_from_refresh_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"], route_class=ApiResponseRoute)


@router.post("/login", response_model=TokenResponse)
def login(login_in: LoginRequest, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, login_in.email)
    if not user or not verify_password(login_in.password, user.password):
        raise UnauthorizedException("邮箱或密码错误")
    token_data = {"user_id": user.id}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_in: RefreshRequest, db: Session = Depends(get_db)):
    user = get_user_from_refresh_token(db, refresh_in.refresh_token)
    token_data = {"user_id": user.id}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )
