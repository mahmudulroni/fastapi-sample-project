import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app.modules.user import service, schemas, models
from app.shared.schemas import Message
from app.api.dependency import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.shared.utils import generate_new_account_email, send_email

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.get("/", response_model=schemas.UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(models.User)
    count = session.exec(count_statement).one()
    statement = select(models.User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return schemas.UsersPublic(data=users, count=count)


@router.post("/", response_model=schemas.UserPublic)
def create_user(*, session: SessionDep, user_in: schemas.UserCreate) -> Any:
    user = service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail="The user with this email already exists in the system.")

    user = service.create_user(session=session, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.patch("/me", response_model=schemas.UserPublic, dependencies=[])
def update_user_me(*, session: SessionDep, user_in: schemas.UserUpdateMe, current_user: CurrentUser) -> Any:
    if user_in.email:
        existing_user = service.get_user_by_email(
            session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists")
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message, dependencies=[])
def update_password_me(*, session: SessionDep, body: schemas.UpdatePassword, current_user: CurrentUser) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one")
    current_user.hashed_password = get_password_hash(body.new_password)
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=schemas.UserPublic, dependencies=[])
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.delete("/me", response_model=Message, dependencies=[])
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves")
    session.delete(current_user)
    session.commit()
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=schemas.UserPublic, dependencies=[])
def register_user(session: SessionDep, user_in: schemas.UserRegister) -> Any:
    user = service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail="The user with this email already exists in the system")
    user_create = schemas.UserCreate.model_validate(user_in)
    user = service.create_user(session=session, user_create=user_create)
    return user


@router.get("/{user_id}", response_model=schemas.UserPublic)
def read_user_by_id(user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    user = session.get(models.User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges")
    return user


@router.patch("/{user_id}", response_model=schemas.UserPublic)
def update_user(*, session: SessionDep, user_id: uuid.UUID, user_in: schemas.UserUpdate) -> Any:
    db_user = session.get(models.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail="The user with this id does not exist in the system")
    if user_in.email:
        existing_user = service.get_user_by_email(
            session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists")
    db_user = service.update_user(
        session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}")
def delete_user(session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID) -> Message:
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves")
    session.exec(delete(models.Item).where(
        col(models.Item.owner_id) == user_id))
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
