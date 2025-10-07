from pydantic import BaseModel
from typing import List, Optional

class SaleItemIn(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    items: List[SaleItemIn]
    discount: float = 0

class SaleOut(BaseModel):
    id: int
    total: float

    class Config:
        from_attributes = True
