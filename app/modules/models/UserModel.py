from typing import Optional
from sqlmodel import SQLModel, Field
from app.shared.base_model import BaseModel


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(default=None, max_length=255)


class User(BaseModel, table=True):
    __tablename__ = "users"
     
    email: str = Field(index=True, unique=True, max_length=255)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(default=None, max_length=255)
