from sqlalchemy.orm import Session

from app.exceptions.handlers import ConflictException, NotFoundException
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleFilter, RoleUpdate


def get_role(db: Session, role_id: int) -> Role | None:
    return db.query(Role).filter(Role.id == role_id).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100, filters: RoleFilter | None = None) -> list[Role]:
    q = db.query(Role)
    if filters and filters.name:
        q = q.filter(Role.name.contains(filters.name))
    return q.offset(skip).limit(limit).all()


def get_role_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()


def create_role(db: Session, role_in: RoleCreate) -> Role:
    existing = get_role_by_name(db, role_in.name)
    if existing:
        raise ConflictException(f"Role with name '{role_in.name}' already exists")
    role = Role(**role_in.model_dump())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, db_role: Role, role_in: RoleUpdate) -> Role:
    update_data = role_in.model_dump(exclude_unset=True)
    if "name" in update_data:
        existing = get_role_by_name(db, update_data["name"])
        if existing and existing.id != db_role.id:
            raise ConflictException(f"Role with name '{update_data['name']}' already exists")
    for field, value in update_data.items():
        setattr(db_role, field, value)
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int) -> None:
    role = get_role(db, role_id)
    if not role:
        raise NotFoundException(f"Role with id {role_id} not found")
    db.delete(role)
    db.commit()
