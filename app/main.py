from fastapi import FastAPI

from app.api.admin import router as admin_router
from app.api.taxonomy import router as taxonomy_router
from app.db import Base, engine

app = FastAPI(title="Home Services Bot Backend", version="0.1.0")

app.include_router(admin_router)
app.include_router(taxonomy_router)


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
