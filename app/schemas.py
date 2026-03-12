from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserUpsert(BaseModel):
    telegram_id: int
    role: str = "client"
    language: str = Field(default="en", pattern="^(en|hi)$")
    is_adult_confirmed: bool = False


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    role: str
    language: str
    is_banned: bool
    is_adult_confirmed: bool


class AdminRoleAssign(BaseModel):
    user_id: int
    role_type: str = Field(pattern="^(super_admin|moderator|content_manager)$")


class AdminRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    role_type: str


class CategoryCreate(BaseModel):
    slug: str
    name_en: str
    name_hi: str
    description: str | None = None


class CategoryRead(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TagCreate(BaseModel):
    slug: str
    name_en: str
    name_hi: str


class TagRead(TagCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MasterServiceCreate(BaseModel):
    name: str
    description: str | None = None
    price_amount: float
    currency: str = "INR"


class MasterProfileCreate(BaseModel):
    display_name: str
    city: str
    district: str
    bio: str | None = None
    online_status: bool = False
    category_ids: list[int] = Field(default_factory=list)
    services: list[MasterServiceCreate] = Field(default_factory=list)


class MasterServiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price_amount: float
    currency: str


class MasterProfileListRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str
    city: str
    district: str
    online_status: bool
    created_at: datetime


class MasterProfileRead(MasterProfileListRead):
    bio: str | None
    services: list[MasterServiceRead]
    category_ids: list[int]


class BookingCreate(BaseModel):
    client_telegram_id: int
    master_id: int
    service_name: str
    scheduled_for: datetime
    notes: str | None = None


class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_user_id: int
    master_id: int
    service_name: str
    scheduled_for: datetime
    notes: str | None
    status: str
    created_at: datetime
