from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.exceptions.handlers import UnauthorizedException
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    user_id: int = getattr(request.state, "user_id", None)
    if user_id is None:
        raise UnauthorizedException("未登录或 token 已过期")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException("用户不存在或已注销")
    return user


def get_user_from_refresh_token(db: Session, token: str) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise UnauthorizedException("无效的刷新凭证")
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise UnauthorizedException("无效的刷新凭证")
    except JWTError:
        raise UnauthorizedException("无效的刷新凭证")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException("用户不存在或已注销")
    return user
