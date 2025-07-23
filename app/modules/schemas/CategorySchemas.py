import uuid
import datetime
from typing import Optional, List
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


class CategoryRead(CategoryBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: Optional[uuid.UUID] = None
    updated_by: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


class CategoriesPublic(BaseModel):
    data: List[CategoryRead]
    count: int
