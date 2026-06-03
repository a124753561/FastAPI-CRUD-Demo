from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.response_route import ApiResponseRoute
from app.database import get_db
from app.exceptions.handlers import NotFoundException
from app.schemas.role import RoleCreate, RoleFilter, RoleResponse, RoleUpdate
from app.services import role as role_service

router = APIRouter(prefix="/roles", tags=["roles"], route_class=ApiResponseRoute)


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role_in: RoleCreate, db: Session = Depends(get_db)):
    return role_service.create_role(db, role_in)


@router.get("/", response_model=list[RoleResponse])
def list_roles(
    skip: int = 0,
    limit: int = 100,
    filters: RoleFilter = Depends(),
    db: Session = Depends(get_db),
):
    return role_service.get_roles(db, skip=skip, limit=limit, filters=filters)


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = role_service.get_role(db, role_id)
    if not role:
        raise NotFoundException(f"Role with id {role_id} not found")
    return role


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_in: RoleUpdate, db: Session = Depends(get_db)):
    db_role = role_service.get_role(db, role_id)
    if not db_role:
        raise NotFoundException(f"Role with id {role_id} not found")
    return role_service.update_role(db, db_role, role_in)


@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role_service.delete_role(db, role_id)
    return None
