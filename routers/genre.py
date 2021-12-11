from fastapi import APIRouter, HTTPException

from database import fetch_query

router = APIRouter(prefix="/genre", tags=["genre"])

QUERY_SELECT = "SELECT * FROM genre;"


@router.get("/", summary="Select genres", description="Retourne les genres d'articles.")
def _select_genres():
    try:
        return fetch_query(QUERY_SELECT)
    except:
        raise HTTPException(status_code=400)
