from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_admin
from app.db import get_db_session
from app.models import AdminRole, User
from app.schemas import AdminRoleAssign, AdminRoleRead, UserRead, UserUpsert

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.post("/users", response_model=UserRead)
async def upsert_user(payload: UserUpsert, db: AsyncSession = Depends(get_db_session)) -> User:
    existing = await db.scalar(select(User).where(User.telegram_id == payload.telegram_id))
    if existing:
        existing.role = payload.role
        existing.language = payload.language
        existing.is_adult_confirmed = payload.is_adult_confirmed
        await db.commit()
        await db.refresh(existing)
        return existing

    user = User(**payload.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/roles", response_model=AdminRoleRead, status_code=status.HTTP_201_CREATED)
async def assign_admin_role(payload: AdminRoleAssign, db: AsyncSession = Depends(get_db_session)) -> AdminRole:
    user = await db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    role = AdminRole(**payload.model_dump())
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


@router.get("/roles", response_model=list[AdminRoleRead])
async def list_admin_roles(db: AsyncSession = Depends(get_db_session)) -> list[AdminRole]:
    items = await db.scalars(select(AdminRole).order_by(AdminRole.id.desc()))
    return list(items)
