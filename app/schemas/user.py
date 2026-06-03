from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=0, le=150)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)

    model_config = ConfigDict(extra="forbid")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
