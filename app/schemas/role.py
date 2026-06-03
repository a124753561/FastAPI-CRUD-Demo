from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RoleCreate(BaseModel):
    name: str = Field(max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)

    @model_validator(mode="before")
    @classmethod
    def check_name(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if not data.get("name", "").strip():
                raise ValueError("角色名不能为空")
        return data


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)

    model_config = ConfigDict(extra="forbid")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("角色名不能为空")
        return v


class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RoleFilter(BaseModel):
    name: Optional[str] = None
