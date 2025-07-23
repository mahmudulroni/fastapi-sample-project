import uuid
from typing import Any
from app.modules.models import PostModel
from app.modules.schemas import PostSchemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func

from app.modules.services import PostService
from app.shared.schemas import Message
from app.dependency import SessionDep, get_current_active_superuser

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.get("/", response_model=PostSchemas.PostsPublic)
def read_posts(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(PostModel.Post)).one()
    posts = PostService.get_all_posts(session, skip, limit)
    return PostSchemas.PostsPublic(data=posts, count=count)


@router.post("/", response_model=PostSchemas.PostRead)
def create_post(session: SessionDep, post_in: PostSchemas.PostCreate) -> Any:
    return PostService.create_post(session, post_in)


@router.get("/{post_id}", response_model=PostSchemas.PostRead)
def get_post(post_id: uuid.UUID, session: SessionDep) -> Any:
    post = PostService.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=PostSchemas.PostRead)
def update_post(post_id: uuid.UUID, post_in: PostSchemas.PostUpdate, session: SessionDep) -> Any:
    db_post = PostService.get_post_by_id(session, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostService.update_post(session, db_post, post_in)


@router.delete("/{post_id}", response_model=Message)
def delete_post(post_id: uuid.UUID, session: SessionDep) -> Any:
    deleted = PostService.delete_post(session, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return Message(message="Post deleted successfully")
