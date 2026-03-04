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
