from fastapi import APIRouter, Depends
from app.api.deps import require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/settings", tags=["settings"]) 

@router.get("/")
async def get_settings(_=Depends(require_roles(UserRole.admin, UserRole.manager))):
    return {"currency": "KES", "tax_rate": 0.0}
