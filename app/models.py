from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class RoleType(str, Enum):
    CLIENT = "client"
    MASTER = "master"
    ADMIN = "admin"


class AdminRoleType(str, Enum):
    SUPER_ADMIN = "super_admin"
    MODERATOR = "moderator"
    CONTENT_MANAGER = "content_manager"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    role: Mapped[str] = mapped_column(String(20), default=RoleType.CLIENT.value)
    language: Mapped[str] = mapped_column(String(2), default="en")
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_adult_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    admin_roles: Mapped[list["AdminRole"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class AdminRole(Base):
    __tablename__ = "admin_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_type", name="uq_user_admin_role"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role_type: Mapped[str] = mapped_column(String(30))

    user: Mapped[User] = relationship(back_populates="admin_roles")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name_en: Mapped[str] = mapped_column(String(120))
    name_hi: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text, default=None)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name_en: Mapped[str] = mapped_column(String(120))
    name_hi: Mapped[str] = mapped_column(String(120))
