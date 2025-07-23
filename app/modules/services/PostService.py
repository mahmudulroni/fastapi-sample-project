from typing import List, Optional
from app.modules.models.PostModel import Post
from sqlmodel import Session, select
from app.modules.schemas import PostSchemas
import uuid


def get_post_by_slug(session: Session, slug: str) -> Optional[Post]:
    statement = select(Post).where(Post.slug == slug)
    return session.exec(statement).first()


def create_post(session: Session, post_in: PostSchemas.PostCreate) -> Post:
    post = Post(**post_in.dict())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_post_by_id(session: Session, post_id: uuid.UUID) -> Optional[Post]:
    return session.get(Post, post_id)


def get_all_posts(session: Session, skip: int = 0, limit: int = 10) -> List[Post]:
    return session.exec(select(Post).offset(skip).limit(limit)).all()


def update_post(session: Session, db_post: Post, post_in: PostSchemas.PostUpdate) -> Post:
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
