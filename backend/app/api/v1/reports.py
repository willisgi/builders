from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from app.api.deps import get_db_session, require_roles
from app.models.user import UserRole

router = APIRouter(prefix="/reports", tags=["reports"]) 

@router.get("/kpis")
async def kpis(db: AsyncSession = Depends(get_db_session), _=Depends(require_roles(UserRole.admin, UserRole.manager))):
    # Simple KPIs: today total sales amount and count
    result = await db.execute(text("""
        SELECT 
            COALESCE(SUM(total),0) as revenue,
            COUNT(*) as sales_count
        FROM sales
        WHERE DATE(created_at) = DATE('now')
    """))
    row = result.mappings().first()
    return {"revenue": float(row["revenue"]), "sales_count": row["sales_count"]}
