from fastapi import APIRouter, HTTPException

from database import fetch_query

router = APIRouter(prefix="/format", tags=["format"])

QUERY_SELECT = "SELECT * FROM format;"


@router.get("/", summary="Select formats", description="Retourne les formats d'articles.")
def _select_formats():
    try:
        return fetch_query(QUERY_SELECT)
    except:
        raise HTTPException(status_code=400)
