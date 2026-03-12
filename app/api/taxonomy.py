from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_admin
from app.db import get_db_session
from app.models import Category, Tag
from app.schemas import CategoryCreate, CategoryRead, TagCreate, TagRead

router = APIRouter(prefix="/taxonomy", tags=["taxonomy"])


@router.get("/categories", response_model=list[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db_session)) -> list[Category]:
    result = await db.scalars(select(Category).order_by(Category.name_en.asc()))
    return list(result)


@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_category(payload: CategoryCreate, db: AsyncSession = Depends(get_db_session)) -> Category:
    category = Category(**payload.model_dump())
    db.add(category)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category slug already exists") from exc
    await db.refresh(category)
    return category


@router.get("/tags", response_model=list[TagRead])
async def list_tags(db: AsyncSession = Depends(get_db_session)) -> list[Tag]:
    result = await db.scalars(select(Tag).order_by(Tag.name_en.asc()))
    return list(result)


@router.post("/tags", response_model=TagRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
async def create_tag(payload: TagCreate, db: AsyncSession = Depends(get_db_session)) -> Tag:
    tag = Tag(**payload.model_dump())
    db.add(tag)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tag slug already exists") from exc
    await db.refresh(tag)
    return tag
