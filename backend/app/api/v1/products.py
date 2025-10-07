from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.models.product import Product
from app.api.deps import get_db_session, require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/products", tags=["products"]) 

@router.get("/", response_model=list[ProductOut])
async def list_products(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Product))
    return [ProductOut.model_validate(p) for p in result.scalars().all()]

@router.post("/", response_model=ProductOut, dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db_session)):
    product = Product(**payload.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return ProductOut.model_validate(product)

@router.patch("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def update_product(product_id: int, payload: ProductUpdate, db: AsyncSession = Depends(get_db_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(product, k, v)
    await db.commit()
    await db.refresh(product)
    return ProductOut.model_validate(product)

@router.delete("/{product_id}", dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager))])
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db_session)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(product)
    await db.commit()
    return {"ok": True}
