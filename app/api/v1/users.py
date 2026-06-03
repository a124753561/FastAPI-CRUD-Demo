from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.response_route import ApiResponseRoute
from app.database import get_db
from app.exceptions.handlers import NotFoundException
from app.schemas.user import UserCreate, UserFilter, UserResponse, UserUpdate
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"], route_class=ApiResponseRoute)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_in)


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 100, filters: UserFilter = Depends(), db: Session = Depends(get_db)):
    return user_service.get_users(db, skip=skip, limit=limit, filters=filters)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise NotFoundException(f"User with id {user_id} not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id)
    if not db_user:
        raise NotFoundException(f"User with id {user_id} not found")
    return user_service.update_user(db, db_user, user_in)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None
