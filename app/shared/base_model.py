import uuid
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import event


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    created_by: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id")
    updated_by: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.id")

    @classmethod
    def __declare_last__(cls):
        if not hasattr(cls, '__table__'):
            return

        @event.listens_for(cls, "before_update", propagate=True)
        def receive_before_update(mapper, connection, target):
            target.updated_at = datetime.now(timezone.utc)
            if hasattr(target, "__current_user__"):
                target.updated_by = target.__current_user__

        @event.listens_for(cls, "before_insert", propagate=True)
        def receive_before_insert(mapper, connection, target):
            now = datetime.now(timezone.utc)
            target.created_at = now
            target.updated_at = now
            if hasattr(target, "__current_user__"):
                target.created_by = target.__current_user__
                target.updated_by = target.__current_user__
