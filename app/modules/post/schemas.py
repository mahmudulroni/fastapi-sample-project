import uuid
import datetime
from typing import Optional, List
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    slug: str
    content: str
    image: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: bool = False
    is_featured: bool = False
    category_id: Optional[uuid.UUID] = None
    created_by: Optional[uuid.UUID] = None
    updated_by: Optional[uuid.UUID] = None
    published_at: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None
    category_id: Optional[uuid.UUID] = None
    updated_by: Optional[uuid.UUID] = None
    published_at: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = None


class PostRead(PostBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class PostsPublic(BaseModel):
    data: List[PostRead]
    count: int
