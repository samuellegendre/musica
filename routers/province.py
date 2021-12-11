from fastapi import APIRouter, HTTPException

from database import fetch_query

router = APIRouter(prefix="/province", tags=["province"])

QUERY_SELECT = "SELECT * FROM province;"


@router.get("/", summary="Select provinces", description="Retourne les provinces.")
def _select_provinces():
    try:
        return fetch_query(QUERY_SELECT)
    except:
        raise HTTPException(status_code=400)
