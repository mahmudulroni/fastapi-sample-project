import uuid
from typing import Any
from app.modules.models import UserModel
from app.modules.schemas import UserSchemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func

from app.modules.services import UserService
from app.modules.shared.schemas import Message
from app.dependency import SessionDep, CurrentUser, get_current_active_superuser
from app.core.security import verify_password, get_password_hash
from app.modules.shared.utils import generate_new_account_email, send_email
from app.core.config import settings

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.get("/", response_model=UserSchemas.UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(
        select(func.count()).select_from(UserModel.User)).one()
    users = session.exec(
        select(UserModel.User).offset(skip).limit(limit)).all()
    return UserSchemas.UsersPublic(data=users, count=count)


@router.post("/", response_model=UserSchemas.UserPublic)
def create_user(*, session: SessionDep, user_in: UserSchemas.UserCreate) -> Any:
    existing = UserService.get_user_by_email(
        session=session, email=user_in.email)
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
