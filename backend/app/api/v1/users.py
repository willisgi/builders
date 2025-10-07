from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.user import UserCreate, UserOut
from app.models.user import User, UserRole
from app.api.deps import get_db_session, require_roles
from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"]) 

@router.get("/", response_model=list[UserOut], dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def list_users(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(User))
    return [UserOut.model_validate(u) for u in result.scalars().all()]

@router.post("/", response_model=UserOut, dependencies=[Depends(require_roles(UserRole.admin))])
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db_session)):
    exists = await db.execute(select(User).where(User.email == payload.email))
    if exists.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="Email already in use")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
        role=payload.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut.model_validate(user)
