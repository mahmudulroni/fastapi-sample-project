import uuid
from typing import Any
from app.modules.models import CategoryModel
from app.modules.schemas import CategorySchemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func
from app.modules.services import CategoryService
from app.shared.schemas import Message
from app.dependency import SessionDep, get_current_active_superuser

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.get("/", response_model=CategorySchemas.CategoriesPublic)
def read_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(
        select(func.count()).select_from(CategoryModel.Category)).one()
    categories = CategoryService.get_all_categories(session, skip, limit)
    return CategorySchemas.CategoriesPublic(data=categories, count=count)


@router.post("/", response_model=CategorySchemas.CategoryRead)
def create_category(session: SessionDep, category_in: CategorySchemas.CategoryCreate) -> Any:
    existing = CategoryService.get_category_by_slug(
        session=session, slug=category_in.slug)
    if existing:
        raise HTTPException(
            status_code=400, detail="Category slug already exists")
    return CategoryService.create_category(session, category_in)


@router.get("/{category_id}", response_model=CategorySchemas.CategoryRead)
def get_category(category_id: uuid.UUID, session: SessionDep) -> Any:
    category = CategoryService.get_category_by_id(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=CategorySchemas.CategoryRead)
def update_category(category_id: uuid.UUID, category_in: CategorySchemas.CategoryUpdate, session: SessionDep) -> Any:
    db_category = CategoryService.get_category_by_id(session, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryService.update_category(session, db_category, category_in)


@router.delete("/{category_id}", response_model=Message)
def delete_category(category_id: uuid.UUID, session: SessionDep) -> Any:
    deleted = CategoryService.delete_category(session, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return Message(message="Category deleted successfully")
