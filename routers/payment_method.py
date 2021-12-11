from fastapi import APIRouter, HTTPException

from database import fetch_query

router = APIRouter(prefix="/payment_method", tags=["payment_method"])

QUERY_SELECT = "SELECT * FROM payment_method;"


@router.get("/", summary="Select payment methods", description="Retourne les méthodes de paiement.")
def _select_payment_methods():
    try:
        return fetch_query(QUERY_SELECT)
    except:
        raise HTTPException(status_code=400)
