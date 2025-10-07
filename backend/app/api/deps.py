from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.models.user import UserRole

bearer = HTTPBearer()

async def get_current_user_role(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> UserRole:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        role_str = payload.get("role")
        if role_str is None:
            raise ValueError("Missing role")
        return UserRole(role_str)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def require_roles(*allowed_roles: UserRole):
    async def dependency(role: UserRole = Depends(get_current_user_role)):
        if role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return role
    return dependency

async def get_db_session(db: AsyncSession = Depends(get_db)):
    return db
