import uuid
from typing import List, Optional
from sqlmodel import Session, select

from app.modules.models.CategoryModel import Category
from app.modules.schemas.CategorySchemas import CategoryCreate, CategoryUpdate


def get_category_by_slug(session: Session, slug: str) -> Optional[Category]:
    statement = select(Category).where(Category.slug == slug)
    return session.exec(statement).first()


def create_category(session: Session, category_in: CategoryCreate) -> Category:
    category = Category(**category_in.dict())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def get_category_by_id(session: Session, category_id: uuid.UUID) -> Optional[Category]:
    return session.get(Category, category_id)


def get_all_categories(session: Session, skip: int = 0, limit: int = 10) -> List[Category]:
    return session.exec(select(Category).offset(skip).limit(limit)).all()


def update_category(session: Session, db_category: Category, category_in: CategoryUpdate) -> Category:
    category_data = category_in.dict(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def delete_category(session: Session, category_id: uuid.UUID) -> bool:
    category = get_category_by_id(session, category_id)
    if not category:
        return False
    session.delete(category)
    session.commit()
    return True
