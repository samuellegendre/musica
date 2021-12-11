from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query
from starlette.requests import Request

from database import fetch_query, execute_query

router = APIRouter(prefix="/orders", tags=["orders"])

QUERY_DELETE = "DELETE FROM orders WHERE id = {};"
QUERY_INSERT = "INSERT INTO orders (employee_id, customer_id, order_date, payment_method_id) " \
               "VALUES ('{0}', '{1}', '{2}', '{3}');"
QUERY_SELECT_COUNT = "SELECT count(*) FROM orders;"
QUERY_SELECT_FROM_SEARCH = "SELECT o.id, concat(c.first_name, ' ', c.last_name) AS customer, o.order_date " \
                           "FROM orders o INNER JOIN customer c on c.id = o.customer_id WHERE cast(o.id AS TEXT) " \
                           "LIKE '{0}' OR lower(c.first_name) LIKE '%{0}%' OR lower(c.last_name) LIKE '%{0}%' " \
                           "OR cast(o.order_date AS TEXT) LIKE '%{0}%' ORDER BY o.id LIMIT 10;"
QUERY_SELECT_ONE = "SELECT o.id, e.id AS employee_id, concat(e.first_name,' ', e.last_name) AS employee, c.id " \
                   "AS customer_id, concat(c.first_name, ' ', c.last_name) AS customer, o.order_date, " \
                   "o.payment_method_id FROM orders o INNER JOIN employee e on e.id = o.employee_id " \
                   "INNER JOIN customer c on c.id = o.customer_id WHERE o.id = {};"
QUERY_SELECT_ROWS = "SELECT o.id, concat(e.first_name, ' ', e.last_name) as employee, concat(c.first_name, ' ', " \
                    "c.last_name) as customer, o.order_date, pm.name as payment_method FROM orders o " \
                    "INNER JOIN employee e on e.id = o.employee_id INNER JOIN customer c on c.id = o.customer_id " \
                    "INNER JOIN payment_method pm on pm.id = o.payment_method_id ORDER BY o.id OFFSET {} LIMIT {};"
QUERY_UPDATE = "UPDATE orders SET employee_id = '{0}', customer_id = '{1}', order_date = '{2}', " \
               "payment_method_id = '{3}' WHERE id = {4};"


@router.get("/", summary="Select orders", description="Retourne toutes les commandes.")
def _select_orders_from_search(q: Optional[str] = Query("", description="Recherche")):
    try:
        return fetch_query(QUERY_SELECT_FROM_SEARCH.format(q.lower()))
    except:
        raise HTTPException(status_code=400)


@router.get("/count", summary="Count orders", description="Retourne le nombre total de commandes.")
def _count_orders():
    try:
        return fetch_query(QUERY_SELECT_COUNT)
    except:
        raise HTTPException(status_code=400)


@router.get("/{id}", summary="Select an order", description="Retourne la commande correspondante.")
def _select_one_order(id: int = Path(..., description="Identifiant de la commande.", example="1", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ONE.format(id))
    except:
        raise HTTPException(status_code=400)


@router.get("/{offset}/{limit}", summary="Select rows of orders", description="Retourne une plage de commandes.")
def _select_rows_orders(offset: int = Path(..., description="Index de départ.", example="0", ge=0),
                        limit: int = Path(..., description="Index de fin.", example="15", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ROWS.format(offset, limit))
    except:
        raise HTTPException(status_code=400)


@router.put("/", status_code=201, summary="Insert order",
            description="Ajoute la commande à la base de données.")
async def _insert_order(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_INSERT.format(request_json["selectOrderEmployee"], request_json["selectOrderCustomer"],
                                          request_json["inputOrderDate"], request_json["selectOrderPaymentMethod"]))
    except:
        raise HTTPException(status_code=400)


@router.patch("/", responses={204: {"model": None}},
              summary="Update order", description="Met à jour les informations d'une commande.")
async def _update_order(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_UPDATE.format(request_json["selectOrderEmployee"], request_json["selectOrderCustomer"],
                                          request_json["inputOrderDate"], request_json["selectOrderPaymentMethod"],
                                          request_json["id"]))
    except:
        raise HTTPException(status_code=400)


@router.delete("/", responses={204: {"model": None}}, summary="Delete order",
               description="Supprime la commande correspondante de la base de données.")
async def _delete_order(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_DELETE.format(request_json["id"]))
    except:
        raise HTTPException(status_code=400)
