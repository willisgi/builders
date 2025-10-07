import asyncio
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.product import Product
from app.models.customer import Customer

PRODUCTS = [
    {"sku": "P001", "name": "Maize Flour 2kg", "price": 250.0, "cost_price": 200.0, "stock_quantity": 80},
    {"sku": "P002", "name": "Sugar 1kg", "price": 180.0, "cost_price": 140.0, "stock_quantity": 120},
    {"sku": "P003", "name": "Cooking Oil 1L", "price": 350.0, "cost_price": 290.0, "stock_quantity": 60},
    {"sku": "P004", "name": "Rice 2kg", "price": 420.0, "cost_price": 360.0, "stock_quantity": 40},
    {"sku": "P005", "name": "Bread", "price": 80.0, "cost_price": 60.0, "stock_quantity": 100},
]

CUSTOMERS = [
    {"name": "John Doe", "phone": "254700000001", "email": "john@example.com"},
    {"name": "Wanjiku", "phone": "254700000002", "email": None},
    {"name": "Otieno", "phone": "254700000003", "email": None},
]

async def seed():
    async with AsyncSessionLocal() as db:
        # Products
        for p in PRODUCTS:
            existing = await db.execute(select(Product).where(Product.sku == p["sku"]))
            if existing.scalar_one_or_none() is None:
                db.add(Product(**p))
        # Customers
        for c in CUSTOMERS:
            existing = await db.execute(select(Customer).where(Customer.phone == c["phone"]))
            if existing.scalar_one_or_none() is None:
                db.add(Customer(**c))
        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())
