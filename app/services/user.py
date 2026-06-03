from typing import Optional

from sqlalchemy.orm import Session

from app.exceptions.handlers import ConflictException, NotFoundException
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise ConflictException(f"User with email '{user_in.email}' already exists")
    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    if "email" in update_data:
        existing = get_user_by_email(db, update_data["email"])
        if existing and existing.id != db_user.id:
            raise ConflictException(f"User with email '{update_data['email']}' already exists")
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    user = get_user(db, user_id)
    if not user:
        raise NotFoundException(f"User with id {user_id} not found")
    db.delete(user)
    db.commit()
