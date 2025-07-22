import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func

from app.modules.post import service, schemas, models
from app.shared.schemas import Message
from app.api.dependency import SessionDep, get_current_active_superuser

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.get("/", response_model=schemas.PostsPublic)
def read_posts(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(models.Post)).one()
    posts = service.get_all_posts(session, skip, limit)
    return schemas.PostsPublic(data=posts, count=count)


@router.post("/", response_model=schemas.PostRead)
def create_post(session: SessionDep, post_in: schemas.PostCreate) -> Any:
    return service.create_post(session, post_in)


@router.get("/{post_id}", response_model=schemas.PostRead)
def get_post(post_id: uuid.UUID, session: SessionDep) -> Any:
    post = service.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=schemas.PostRead)
def update_post(post_id: uuid.UUID, post_in: schemas.PostUpdate, session: SessionDep) -> Any:
    db_post = service.get_post_by_id(session, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return service.update_post(session, db_post, post_in)


@router.delete("/{post_id}", response_model=Message)
def delete_post(post_id: uuid.UUID, session: SessionDep) -> Any:
    deleted = service.delete_post(session, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return Message(message="Post deleted successfully")
