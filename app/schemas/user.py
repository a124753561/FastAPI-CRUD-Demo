from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


class UserCreate(BaseModel):
    name: str = Field(max_length=100)
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=0, le=150)
    role_id: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def check_name(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("name", "").strip():
                raise ValueError("姓名不能为空")
        return data


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)
    role_id: Optional[int] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("姓名不能为空")
        return v


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    role_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserFilter(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
