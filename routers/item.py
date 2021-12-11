from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query
from starlette.requests import Request

from database import fetch_query, execute_query

router = APIRouter(prefix="/item", tags=["item"])

QUERY_DELETE = "DELETE FROM item WHERE id = {};"
QUERY_INSERT = "INSERT INTO item (title, artist, release_date, format_id, genre_id, price, quantity) " \
               "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');"
QUERY_SELECT_COUNT = "SELECT count(*) FROM item;"
QUERY_SELECT_FROM_SEARCH = "SELECT i.id, i.title, i.artist, i.release_date, f.name AS format, g.name " \
                           "AS genre, i.price, i.quantity FROM item i INNER JOIN format f on f.id = i.format_id " \
                           "INNER JOIN genre g on g.id = i.genre_id WHERE cast(i.id AS TEXT) LIKE '{0}' " \
                           "OR lower(i.title) LIKE '%{0}%' OR lower(i.artist) LIKE '%{0}%' ORDER BY id LIMIT 10;"
QUERY_SELECT_ONE = "SELECT * FROM item WHERE id = {}"
QUERY_SELECT_ROWS = "SELECT i.id, i.title, i.artist, i.release_date, f.name AS format, g.name " \
                    "AS genre, i.price, i.quantity FROM item i INNER JOIN format f on f.id = i.format_id " \
                    "INNER JOIN genre g on g.id = i.genre_id ORDER BY id OFFSET {} LIMIT {};"
QUERY_UPDATE = "UPDATE item SET title = '{0}', artist = '{1}', release_date = '{2}', format_id = '{3}', " \
               "genre_id = '{4}', price = '{5}', quantity = '{6}' WHERE id = {7};"


@router.get("/", summary="Select items", description="Retourne tous les articles.")
def _select_item_from_search(q: Optional[str] = Query("", description="Recherche.")):
    try:
        return fetch_query(QUERY_SELECT_FROM_SEARCH.format(q.lower()))
    except:
        raise HTTPException(status_code=400)


@router.get("/count", summary="Count items", description="Retourne le nombre total d'articles.")
def _count_items():
    try:
        return fetch_query(QUERY_SELECT_COUNT)
    except:
        raise HTTPException(status_code=400)


@router.get("/{id}", summary="Select an item", description="Retourne l'article correspondant.")
def _select_one_item(id: int = Path(..., description="Identifiant de l'article.", example="1", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ONE.format(id))
    except:
        raise HTTPException(status_code=400)


@router.get("/{offset}/{limit}", summary="Select rows of items", description="Retourne une plage d'articles.")
def _select_rows_items(offset: int = Path(..., description="Index de départ.", example="0", ge=0),
                       limit: int = Path(..., description="Index de fin.", example="15", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ROWS.format(offset, limit))
    except:
        raise HTTPException(status_code=400)


@router.put("/", status_code=201,
            summary="Insert item", description="Ajoute le nouvel article dans la base de données.")
async def _insert_item(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_INSERT.format(request_json["inputItemTitle"], request_json["inputItemArtist"],
                                          request_json["inputItemReleaseDate"], request_json["selectItemFormat"],
                                          request_json["selectItemGenre"], request_json["inputItemPrice"],
                                          request_json["inputItemAvailableQuantity"]))
    except:
        raise HTTPException(status_code=400)


@router.patch("/", responses={204: {"model": None}}, summary="Update item",
              description="Met à jour les informations de l'article correspondant.")
async def _update_item(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_UPDATE.format(request_json["inputItemTitle"], request_json["inputItemArtist"],
                                          request_json["inputItemReleaseDate"], request_json["selectItemFormat"],
                                          request_json["selectItemGenre"], request_json["inputItemPrice"],
                                          request_json["inputItemAvailableQuantity"], request_json["id"]))
    except:
        raise HTTPException(status_code=400)


@router.delete("/", responses={204: {"model": None}}, summary="Delete item",
               description="Supprime l'article correspondant de la base de données.")
async def _delete_item(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_DELETE.format(request_json["id"]))
    except:
        raise HTTPException(status_code=400)
