import uuid
import datetime

from typing import Optional, List
from sqlalchemy import Column, JSON
from sqlmodel import Field

from app.modules.shared.base_model import BaseModel


class Post(BaseModel, table=True):
    __tablename__ = "posts"

    title: str = Field(index=True, max_length=255)
    slug: str = Field(index=True, unique=True, max_length=255)
    content: str = Field(default="", max_length=10000)
    image: Optional[str] = Field(default=None, max_length=1024)
    thumbnail_url: Optional[str] = Field(default=None, max_length=1024)
    is_published: bool = Field(default=False)
    is_featured: bool = Field(default=False)
    category_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="categories.id")
    published_at: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = Field(
        default=None, sa_column=Column(JSON, nullable=True)
    )
