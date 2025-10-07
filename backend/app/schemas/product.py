from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    sku: str
    name: str
    price: float
    cost_price: Optional[float] = None
    stock_quantity: int = 0
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
