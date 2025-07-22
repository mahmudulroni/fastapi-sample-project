from typing import Optional
from sqlmodel import Session
from app.modules.user import models, schemas
from app.core.security import get_password_hash


def get_user_by_email(session: Session, email: str) -> Optional[models.User]:
    return session.exec(
        models.User.select().where(models.User.email == email)
    ).first()


def create_user(session: Session, user_create: schemas.UserCreate) -> models.User:
    db_obj = models.User(
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        full_name=user_create.full_name,
        is_active=True,
        is_superuser=user_create.is_superuser or False
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(session: Session, db_user: models.User, user_in: schemas.UserUpdate) -> models.User:
    user_data = user_in.dict(exclude_unset=True)
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(
            user_data.pop("password"))
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
