from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_admin
from app.db import get_db_session
from app.models import AdminRole, MasterCategory, MasterProfile, MasterService, User
from app.schemas import (
    AdminRoleAssign,
    AdminRoleRead,
    MasterProfileCreate,
    MasterProfileRead,
    MasterServiceRead,
    UserRead,
    UserUpsert,
)

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


@router.post("/masters", response_model=MasterProfileRead, status_code=status.HTTP_201_CREATED)
async def create_master_profile(payload: MasterProfileCreate, db: AsyncSession = Depends(get_db_session)) -> MasterProfileRead:
    master = MasterProfile(
        display_name=payload.display_name,
        city=payload.city,
        district=payload.district,
        bio=payload.bio,
        online_status=payload.online_status,
    )
    db.add(master)
    await db.flush()

    for category_id in payload.category_ids:
        db.add(MasterCategory(master_id=master.id, category_id=category_id))

    for service in payload.services:
        db.add(MasterService(master_id=master.id, **service.model_dump()))

    await db.commit()
    await db.refresh(master)
    await db.refresh(master, attribute_names=["services", "categories"])

    return MasterProfileRead(
        id=master.id,
        display_name=master.display_name,
        city=master.city,
        district=master.district,
        online_status=master.online_status,
        created_at=master.created_at,
        bio=master.bio,
        services=[MasterServiceRead.model_validate(item) for item in master.services],
        category_ids=[item.category_id for item in master.categories],
    )
