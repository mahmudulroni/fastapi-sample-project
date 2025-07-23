import uuid
from typing import Any
from app.modules.models import UserModel
from app.modules.schemas import UserSchemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func

from app.modules.services import UserService
from app.shared.schemas import Message
from app.dependency import SessionDep, CurrentUser, get_current_active_superuser
from app.core.security import verify_password, get_password_hash
from app.shared.utils import generate_new_account_email, send_email
from app.core.config import settings

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.get("/", response_model=UserSchemas.UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(select(func.count()).select_from(UserModel.User)).one()
    users = session.exec(select(UserModel.User).offset(skip).limit(limit)).all()
    return UserSchemas.UsersPublic(data=users, count=count)


@router.post("/", response_model=UserSchemas.UserPublic)
def create_user(*, session: SessionDep, user_in: UserSchemas.UserCreate) -> Any:
    existing = UserService.get_user_by_email(session=session, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=400, detail="User with this email already exists")
    user = UserService.create_user(session=session, user_create=user_in)
    if settings.emails_enabled:
        email_data = generate_new_account_email(
            email_to=user.email, username=user.email, password=user_in.password)
        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.patch("/me", response_model=UserSchemas.UserPublic, dependencies=[])
def update_user_me(*, session: SessionDep, user_in: UserSchemas.UserUpdateMe, current_user: CurrentUser) -> Any:
    if user_in.email:
        existing_user = UserService.get_user_by_email(
            session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists")
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message, dependencies=[])
def update_password_me(*, session: SessionDep, body: UserSchemas.UpdatePassword, current_user: CurrentUser) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one")
    current_user.hashed_password = get_password_hash(body.new_password)
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserSchemas.UserPublic, dependencies=[])
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


@router.post("/signup", response_model=UserSchemas.UserPublic, dependencies=[])
def register_user(session: SessionDep, user_in: UserSchemas.UserCreate) -> Any:
    user = UserService.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists")
    user = UserService.create_user(session=session, user_create=user_in)
    return user


@router.get("/{user_id}", response_model=UserSchemas.UserPublic)
def read_user_by_id(user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser) -> Any:
    user = session.get(UserModel.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user or current_user.is_superuser:
        return user
    raise HTTPException(status_code=403, detail="Not enough privileges")


@router.patch("/{user_id}", response_model=UserSchemas.UserPublic)
def update_user(*, session: SessionDep, user_id: uuid.UUID, user_in: UserSchemas.UserUpdate) -> Any:
    db_user = session.get(UserModel.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.email:
        existing_user = UserService.get_user_by_email(
            session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists")
    user = UserService.update_user(
        session=session, db_user=db_user, user_in=user_in)
    return user


@router.delete("/{user_id}", response_model=Message)
def delete_user(session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID) -> Any:
    user = session.get(UserModel.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves")
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
