from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.admin import router as admin_router
from app.api.bookings import router as bookings_router
from app.api.catalog import router as catalog_router
from app.api.taxonomy import router as taxonomy_router
from app.db import Base, engine
from app.webapp import router as webapp_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Home Services Bot Backend", version="0.1.0", lifespan=lifespan)

app.include_router(admin_router)
app.include_router(bookings_router)
app.include_router(catalog_router)
app.include_router(taxonomy_router)
app.include_router(webapp_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
