from typing import List, Optional
from sqlmodel import Session, select
from app.modules.post import models, schemas
import uuid


def create_post(session: Session, post_in: schemas.PostCreate) -> models.Post:
    post = models.Post(**post_in.dict())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_post_by_id(session: Session, post_id: uuid.UUID) -> Optional[models.Post]:
    return session.get(models.Post, post_id)


def get_all_posts(session: Session, skip: int = 0, limit: int = 10) -> List[models.Post]:
    return session.exec(select(models.Post).offset(skip).limit(limit)).all()


def update_post(session: Session, db_post: models.Post, post_in: schemas.PostUpdate) -> models.Post:
    post_data = post_in.dict(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


def delete_post(session: Session, post_id: uuid.UUID) -> bool:
    post = get_post_by_id(session, post_id)
    if not post:
        return False
    session.delete(post)
    session.commit()
    return True
