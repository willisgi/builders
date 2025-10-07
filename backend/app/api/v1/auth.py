from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user import UserLogin, UserOut
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == payload.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(subject=str(user.id), extra_claims={"role": user.role.value})
    return {"access_token": token, "token_type": "bearer", "user": UserOut.model_validate(user)}
