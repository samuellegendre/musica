from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query
from starlette.requests import Request

from database import fetch_query, execute_query

router = APIRouter(prefix="/employee", tags=["employee"])

QUERY_DELETE = "DELETE FROM employee WHERE id = {};"
QUERY_INSERT = "INSERT INTO employee (first_name, last_name, phone, hire_date) VALUES ('{0}', '{1}', '{2}', '{3}');"
QUERY_SELECT_COUNT = "SELECT count(*) FROM employee;"
QUERY_SELECT_FROM_SEARCH = "SELECT * FROM employee WHERE cast(id AS TEXT) LIKE '{0}' OR lower(first_name) " \
                           "LIKE '%{0}%' or lower(last_name) LIKE '%{0}%' ORDER BY id LIMIT 10;"
QUERY_SELECT_ONE = "SELECT * FROM employee WHERE id = {}"
QUERY_SELECT_ROWS = "SELECT * FROM employee ORDER BY id OFFSET {} LIMIT {};"
QUERY_UPDATE = "UPDATE employee SET first_name = '{0}', last_name = '{1}', phone = '{2}', hire_date = '{3}' " \
               "WHERE id = {4};"


@router.get("/", summary="Select employees", description="Retournes tous les employés.")
def _select_employees_from_search(q: Optional[str] = Query("", description="Recherche.")):
    try:
        return fetch_query(QUERY_SELECT_FROM_SEARCH.format(q.lower()))
    except:
        raise HTTPException(status_code=400)


@router.get("/count", summary="Count employees", description="Retourne le nombre total d'employés.")
def _count_employees():
    try:
        return fetch_query(QUERY_SELECT_COUNT)
    except:
        raise HTTPException(status_code=400)


@router.get("/{id}", summary="Select an employee", description="Retourne l'employé correspondant.")
def _select_one_employee(id: int = Path(..., description="Index de départ.", example="1", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ONE.format(id))
    except:
        raise HTTPException(status_code=400)


@router.get("/{offset}/{limit}", summary="Select rows of employees", description="Retourne une plage d'employés.")
def _select_rows_employees(offset: int = Path(..., description="Index de départ.", example="0", ge=0),
                           limit: int = Path(..., description="Index de fin.", example="15", ge=1)):
    try:
        return fetch_query(QUERY_SELECT_ROWS.format(offset, limit))
    except:
        raise HTTPException(status_code=400)


@router.put("/", status_code=201, summary="Insert employee",
            description="Ajoute le nouvel employé dans la base de données.")
async def _insert_employee(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_INSERT.format(request_json["inputEmployeeFirstName"], request_json["inputEmployeeLastName"],
                                          request_json["inputEmployeePhoneNumber"],
                                          request_json["inputEmployeeHireDate"]))
    except:
        raise HTTPException(status_code=400)


@router.patch("/", responses={204: {"model": None}}, summary="Update employee",
              description="Met à jour les informations de l'employé correspondant.")
async def _update_employee(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_UPDATE.format(request_json["inputEmployeeFirstName"], request_json["inputEmployeeLastName"],
                                          request_json["inputEmployeePhoneNumber"],
                                          request_json["inputEmployeeHireDate"], request_json["id"]))
    except:
        raise HTTPException(status_code=400)


@router.delete("/", responses={204: {"model": None}}, summary="Delete employee",
               description="Supprime l'employé correspondant de la base de données.")
async def _delete_employee(request: Request):
    try:
        request_json = await request.json()
        execute_query(QUERY_DELETE.format(request_json["id"]))
    except:
        raise HTTPException(status_code=400)
