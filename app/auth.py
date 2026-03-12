from fastapi import Depends, Header, HTTPException, status

from app.config import settings


async def require_admin(x_admin_token: str = Header(default="")) -> None:
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin token")


AdminOnly = Depends(require_admin)
