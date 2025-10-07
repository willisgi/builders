from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.sale import SaleCreate, SaleOut
from app.models.sale import Sale, SaleItem
from app.models.product import Product
from app.api.deps import get_db_session, require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/sales", tags=["sales"]) 

@router.post("/", response_model=SaleOut, dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager, UserRole.cashier))])
async def create_sale(payload: SaleCreate, db: AsyncSession = Depends(get_db_session)):
    # Calculate totals and validate stock
    subtotal = 0
    for item in payload.items:
        product = await db.get(Product, item.product_id)
        if product is None:
            raise HTTPException(status_code=400, detail=f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        subtotal += item.quantity * item.unit_price

    total = max(subtotal - payload.discount, 0)

    sale = Sale(customer_id=payload.customer_id, subtotal=subtotal, discount=payload.discount, total=total)
    db.add(sale)
    await db.flush()

    for item in payload.items:
        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=item.quantity * item.unit_price,
        )
        db.add(sale_item)
        # decrement stock
        product = await db.get(Product, item.product_id)
        product.stock_quantity -= item.quantity

    await db.commit()
    await db.refresh(sale)
    return SaleOut(id=sale.id, total=float(sale.total))
