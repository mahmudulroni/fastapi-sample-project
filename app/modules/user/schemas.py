import uuid
from pydantic import EmailStr
from typing import Optional, List
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)
    full_name: Optional[str] = None


class UserUpdateMe(SQLModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UsersPublic(SQLModel):
    data: List[UserPublic]
    count: int
