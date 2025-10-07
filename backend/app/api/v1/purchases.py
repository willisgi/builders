from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.purchase import PurchaseCreate, PurchaseOut
from app.models.purchase import Purchase
from app.api.deps import get_db_session, require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/purchases", tags=["purchases"]) 

@router.post("/", response_model=PurchaseOut, dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def create_purchase(payload: PurchaseCreate, db: AsyncSession = Depends(get_db_session)):
    purchase = Purchase(**payload.model_dump())
    db.add(purchase)
    await db.commit()
    await db.refresh(purchase)
    return PurchaseOut.model_validate(purchase)
