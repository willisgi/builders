from pydantic import BaseModel

class PurchaseCreate(BaseModel):
    supplier: str
    total_cost: float

class PurchaseOut(BaseModel):
    id: int
    supplier: str
    total_cost: float

    class Config:
        from_attributes = True
