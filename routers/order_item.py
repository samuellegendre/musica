from fastapi import APIRouter, HTTPException, Path
from starlette.requests import Request

from database import fetch_query, execute_query

router = APIRouter(prefix="/order_item", tags=["order_item"])

QUERY_DELETE = "DELETE FROM order_item WHERE id = {};"
QUERY_INSERT = "INSERT INTO order_item (order_id, item_id, quantity) VALUES ('{0}', '{1}', '{2}');"
QUERY_SELECT_COUNT = "SELECT count(*) FROM order_item;"
QUERY_SELECT_ONE = "SELECT oi.id, o.id as order_id, concat(o.order_date, ' ', c.first_name, ' ', c.last_name) " \
                   "as order, i.id as item_id, concat(i.title, ' par ', i.artist, ' (', f.name, ')') " \
                   "as item, oi.quantity FROM order_item oi INNER JOIN orders o on o.id = oi.order_id " \
                   "INNER JOIN customer c on c.id = o.customer_id INNER JOIN item i on i.id = oi.item_id " \
                   "INNER JOIN format f on f.id = i.format_id WHERE oi.id = {};"
QUERY_SELECT_ROWS = "SELECT order_item.id, concat('#', o.id, ' | ', o.order_date, ' ', c.first_name, ' ', " \
                    "c.last_name) AS orders, concat('#', i.id, ' | ', i.title, ' par ', i.artist, ' (', f.name, ')') " \
                    "AS item, order_item.quantity FROM order_item INNER JOIN item i on i.id = order_item.item_id " \
                    "INNER JOIN orders o on o.id = order_item.order_id INNER JOIN customer c on c.id = o.customer_id " \
                    "INNER JOIN format f on f.id = i.format_id ORDER BY order_item.id OFFSET {} LIMIT {};"
QUERY_UPDATE = "UPDATE order_item SET order_id = '{0}', item_id = '{1}', quantity = '{2}' WHERE id = {3};"


@router.get("/count", summary="Count orders' items", description="Retourne le nombre total d'articles des commandes.")
def _count_order_items():
    try:
        return fetch_query(QUERY_SELECT_COUNT)
    except:
        raise HTTPException(status_code=400)


@router.get("/{id}", summary="Select an order's item", description="Retourne un article d'une commande.")
def _select_one_order_item(
        id: int = Path(..., description="Identifiant de l'article de la commande.", example="1", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ONE.format(id))
    except:
        raise HTTPException(status_code=400)


@router.get("/{offset}/{limit}", summary="Select rows of orders' items",
            description="Retourne une plage d'articles des commandes.")
def _select_rows_order_items(offset: int = Path(..., description="Index de départ.", example="0", ge=0),
                             limit: int = Path(..., description="Index de fin.", example="15", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ROWS.format(offset, limit))
    except:
        raise HTTPException(status_code=400)


@router.put("/", status_code=201, summary="Insert an item from an order",
            description="Ajoute le nouvel article d'une commande à la base de données.")
async def _insert_order_item(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_INSERT.format(request_json["selectItemOrderOrderId"], request_json["selectItemOrderItemId"],
                                          request_json["inputItemOrderQuantity"]))
    except:
        HTTPException(status_code=400)


@router.patch("/", responses={204: {"model": None}}, summary="Update an item from an order",
              description="Met à jour les informations d'un article d'une commande correspondant.")
async def _update_order_item(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_UPDATE.format(request_json["selectItemOrderOrderId"], request_json["selectItemOrderItemId"],
                                          request_json["inputItemOrderQuantity"], request_json["id"]))
    except:
        raise HTTPException(status_code=400)


@router.delete("/", responses={204: {"model": None}}, summary="Delete an item from an order",
               description="Supprime l'article d'une commande correspondant de la base de données.")
async def _delete_order_item(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_DELETE.format(request_json["id"]))
    except:
        raise HTTPException(status_code=400)
