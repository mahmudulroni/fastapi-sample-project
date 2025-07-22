from typing import Optional
from sqlmodel import Field

from app.shared.base_model import BaseModel


class Category(BaseModel, table=True):
    __tablename__ = "categories"

    name: str = Field(index=True, max_length=255)
    slug: str = Field(index=True, unique=True, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    image: Optional[str] = Field(default=None, max_length=1024)
