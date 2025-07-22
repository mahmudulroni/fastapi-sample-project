import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func
from app.modules.category import service, schemas, models
from app.shared.schemas import Message
from app.api.dependency import SessionDep, get_current_active_superuser

router = APIRouter(dependencies=[Depends(get_current_active_superuser)])


@router.get("/", response_model=schemas.CategoriesPublic)
def read_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count = session.exec(
        select(func.count()).select_from(models.Category)).one()
    categories = service.get_all_categories(session, skip, limit)
    return schemas.CategoriesPublic(data=categories, count=count)


@router.post("/", response_model=schemas.CategoryRead)
def create_category(session: SessionDep, category_in: schemas.CategoryCreate) -> Any:
    return service.create_category(session, category_in)


@router.get("/{category_id}", response_model=schemas.CategoryRead)
def get_category(category_id: uuid.UUID, session: SessionDep) -> Any:
    category = service.get_category_by_id(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch("/{category_id}", response_model=schemas.CategoryRead)
def update_category(category_id: uuid.UUID, category_in: schemas.CategoryUpdate, session: SessionDep) -> Any:
    db_category = service.get_category_by_id(session, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return service.update_category(session, db_category, category_in)


@router.delete("/{category_id}", response_model=Message)
def delete_category(category_id: uuid.UUID, session: SessionDep) -> Any:
    deleted = service.delete_category(session, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return Message(message="Category deleted successfully")
