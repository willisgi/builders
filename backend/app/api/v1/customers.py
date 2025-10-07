from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut
from app.models.customer import Customer
from app.api.deps import get_db_session, require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/customers", tags=["customers"]) 

@router.get("/", response_model=list[CustomerOut])
async def list_customers(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Customer))
    return [CustomerOut.model_validate(c) for c in result.scalars().all()]

@router.post("/", response_model=CustomerOut, dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def create_customer(payload: CustomerCreate, db: AsyncSession = Depends(get_db_session)):
    customer = Customer(**payload.model_dump())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return CustomerOut.model_validate(customer)

@router.patch("/{customer_id}", response_model=CustomerOut, dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def update_customer(customer_id: int, payload: CustomerUpdate, db: AsyncSession = Depends(get_db_session)):
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(customer, k, v)
    await db.commit()
    await db.refresh(customer)
    return CustomerOut.model_validate(customer)

@router.delete("/{customer_id}", dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def delete_customer(customer_id: int, db: AsyncSession = Depends(get_db_session)):
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    await db.delete(customer)
    await db.commit()
    return {"ok": True}
