from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import String, asc, cast, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db_session
from app.models import MasterProfile
from app.schemas import MasterProfileListRead, MasterProfileRead, MasterServiceRead

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/masters", response_model=list[MasterProfileListRead])
async def list_masters(
    db: AsyncSession = Depends(get_db_session),
    city: str | None = Query(default=None),
    q: str | None = Query(default=None),
    sort: str = Query(default="newest", pattern="^(newest|name_asc)$"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[MasterProfile]:
    query = select(MasterProfile)

    if city:
        query = query.where(func.lower(MasterProfile.city) == city.lower())

    if q:
        token = f"%{q.lower()}%"
        query = query.where(
            or_(
                func.lower(MasterProfile.display_name).like(token),
                func.lower(cast(MasterProfile.bio, String)).like(token)
            )
        )

    ordering = desc(MasterProfile.created_at) if sort == "newest" else asc(MasterProfile.display_name)
    query = query.order_by(ordering).offset(offset).limit(limit)

    result = await db.scalars(query)
    return list(result)


@router.get("/masters/{master_id}", response_model=MasterProfileRead)
async def get_master(master_id: int, db: AsyncSession = Depends(get_db_session)) -> MasterProfileRead:
    query = (
        select(MasterProfile)
        .options(selectinload(MasterProfile.services), selectinload(MasterProfile.categories))
        .where(MasterProfile.id == master_id)
    )
    master = await db.scalar(query)
    if not master:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Master not found")

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
