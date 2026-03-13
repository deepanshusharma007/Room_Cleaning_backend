from fastapi import APIRouter, Depends, Query
from app.database import supabase
from app.auth import verify_token

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/receipts")
def get_receipts(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    admin=Depends(verify_token)
):

    start = (page - 1) * limit
    end = start + limit - 1

    response = supabase.table("cleaning_receipts") \
        .select("*", count="exact") \
        .range(start, end) \
        .order("created_at", desc=True) \
        .execute()

    return {
        "data": response.data,
        "total": response.count,
        "page": page,
        "limit": limit
    }