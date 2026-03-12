from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.models import BookingRequest, BookingStatus, MasterProfile, RoleType, User
from app.schemas import BookingCreate, BookingRead

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(payload: BookingCreate, db: AsyncSession = Depends(get_db_session)) -> BookingRequest:
    master = await db.get(MasterProfile, payload.master_id)
    if not master:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Master not found")

    user = await db.scalar(select(User).where(User.telegram_id == payload.client_telegram_id))
    if not user:
        user = User(telegram_id=payload.client_telegram_id, role=RoleType.CLIENT.value, is_adult_confirmed=True)
        db.add(user)
        await db.flush()

    booking = BookingRequest(
        client_user_id=user.id,
        master_id=payload.master_id,
        service_name=payload.service_name,
        scheduled_for=payload.scheduled_for,
        notes=payload.notes,
        status=BookingStatus.NEW.value,
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking


@router.get("/by-client/{telegram_id}", response_model=list[BookingRead])
async def list_client_bookings(telegram_id: int, db: AsyncSession = Depends(get_db_session)) -> list[BookingRequest]:
    user = await db.scalar(select(User).where(User.telegram_id == telegram_id))
    if not user:
        return []

    rows = await db.scalars(
        select(BookingRequest)
        .where(BookingRequest.client_user_id == user.id)
        .order_by(BookingRequest.created_at.desc())
    )
    return list(rows)


@router.post("/{booking_id}/cancel", response_model=BookingRead)
async def cancel_booking(booking_id: int, db: AsyncSession = Depends(get_db_session)) -> BookingRequest:
    booking = await db.get(BookingRequest, booking_id)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    booking.status = BookingStatus.CANCELED.value
    await db.commit()
    await db.refresh(booking)
    return booking
