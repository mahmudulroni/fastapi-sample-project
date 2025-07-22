import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# ------------------------
# User Input Schemas
# ------------------------

class UserCreate(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


UserRegister = UserCreate


class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


# ------------------------
# Password Management Schemas
# ------------------------

class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# ------------------------
# Public Output Schemas
# ------------------------

class UserPublic(SQLModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    full_name: str | None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
