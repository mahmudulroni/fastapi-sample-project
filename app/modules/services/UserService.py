from typing import Optional
from app.modules.models.UserModel import User
from sqlmodel import select, Session
from app.modules.schemas import UserSchemas
from app.core.security import get_password_hash


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(session: Session, user_create: UserSchemas.UserCreate) -> User:
    db_obj = User(
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


def update_user(session: Session, db_user: User, user_in: UserSchemas.UserUpdate) -> User:
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
