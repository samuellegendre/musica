from typing import Optional

from fastapi import Path, HTTPException, APIRouter, Query
from starlette.requests import Request

from database import fetch_query, execute_query

router = APIRouter(prefix="/customer", tags=["customer"])

QUERY_DELETE = "DELETE FROM customer WHERE id = {};"
QUERY_INSERT = "INSERT INTO customer (first_name, last_name, phone, street, city, province_id, postal_code) VALUES " \
               "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');"
QUERY_SELECT_COUNT = "SELECT count(*) FROM customer;"
QUERY_SELECT_FROM_SEARCH = "SELECT * FROM customer WHERE cast(id AS TEXT) LIKE '{0}' OR lower(first_name) " \
                           "LIKE '%{0}%' or lower(last_name) LIKE '%{0}%' ORDER BY id LIMIT 10;"
QUERY_SELECT_ONE = "SELECT * from customer WHERE id = {}"
QUERY_SELECT_ROWS = "SELECT c.id, c.first_name, c.last_name, c.phone, concat(c.street, ', ', c.city, ' (', p.name, " \
                    "') ', c.postal_code) as address FROM customer c INNER JOIN province p on p.id = c.province_id " \
                    "ORDER BY c.id OFFSET {} LIMIT {};"
QUERY_UPDATE = "UPDATE customer SET first_name = '{0}', last_name = '{1}', phone = '{2}', street  = '{3}', " \
               "city = '{4}', province_id = '{5}', postal_code = '{6}' WHERE id = {7};"


@router.get("/", summary="Select customers", description="Retourne tous les clients.")
def _select_customers_from_search(q: Optional[str] = Query("", description="Recherche.")):
    try:
        return fetch_query(QUERY_SELECT_FROM_SEARCH.format(q))
    except:
        raise HTTPException(status_code=400)


@router.get("/count", summary="Count customers", description="Retourne le nombre total de clients.")
def _count_customers():
    try:
        return fetch_query(QUERY_SELECT_COUNT)
    except:
        raise HTTPException(status_code=400)


@router.get("/{id}", summary="Select a customer", description="Retourne le client correspondant.")
def _select_one_customer(id: int = Path(..., description="Identifiant du client", example="1", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ONE.format(id))
    except:
        raise HTTPException(status_code=400)


@router.get("/{offset}/{limit}", summary="Select rows of customers", description="Retourne une plage de clients.")
def _select_rows_customers(offset: int = Path(..., description="Index de départ.", example="0", ge=0),
                           limit: int = Path(..., description="Index de fin.", example="15", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ROWS.format(offset, limit))
    except:
        raise HTTPException(status_code=400)


@router.put("/", status_code=201, summary="Insert customer",
            description="Ajoute le nouveau client dans la base de données.")
async def _insert_customer(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_INSERT.format(request_json["inputCustomerFirstName"], request_json["inputCustomerLastName"],
                                          request_json["inputCustomerPhoneNumber"], request_json["inputCustomerRoad"],
                                          request_json["inputCustomerCity"], request_json["selectCustomerProvince"],
                                          request_json["inputCustomerPostalCode"]))
    except:
        raise HTTPException(status_code=400)


@router.patch("/", responses={204: {"model": None}}, summary="Update customer",
              description="Met à jour les informations du client correspondant.")
async def _update_customer(request: Request):
    try:
        request_json = await request.json()
        execute_query(
            QUERY_UPDATE.format(request_json["inputCustomerFirstName"], request_json["inputCustomerLastName"],
                                request_json["inputCustomerPhoneNumber"], request_json["inputCustomerRoad"],
                                request_json["inputCustomerCity"], request_json["selectCustomerProvince"],
                                request_json["inputCustomerPostalCode"], request_json["id"]))
    except:
        raise HTTPException(status_code=400)


@router.delete("/", responses={204: {"model": None}}, summary="Delete customer",
               description="Supprime le client correspondant de la base de données.")
async def _delete_customer(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_DELETE.format(request_json["id"]))
    except:
        raise HTTPException(status_code=400)
