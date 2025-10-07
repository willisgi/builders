from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.services.mpesa import stk_push, stk_query
from app.api.deps import require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/mpesa", tags=["mpesa"]) 

class StkPushRequest(BaseModel):
    phone_number: str
    amount: int
    account_reference: str = "POS"
    transaction_desc: str = "Sale payment"

@router.post("/stk", dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager, UserRole.cashier))])
async def create_stk(payload: StkPushRequest):
    data = await stk_push(
        phone_number=payload.phone_number,
        amount=payload.amount,
        account_reference=payload.account_reference,
        transaction_desc=payload.transaction_desc,
    )
    return data

@router.post("/callback")
async def mpesa_callback(request: Request):
    # Accept callbacks from Daraja (no auth). In production, validate origin/signatures.
    payload = await request.json()
    # For now, simply acknowledge success to Daraja
    return {"ResultCode": 0, "ResultDesc": "Success"}

class VerifyRequest(BaseModel):
    checkout_request_id: str

@router.post("/verify", dependencies=[Depends(require_roles(UserRole.admin, UserRole.manager, UserRole.cashier))])
async def verify_stk(payload: VerifyRequest):
    data = await stk_query(payload.checkout_request_id)
    return data
