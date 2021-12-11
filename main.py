from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import customer, item, employee, order_item, orders, format, genre, payment_method, province

_tags_metadata = [
    {
        "name": "customer",
        "description": "Endpoints qui gèrent les clients."
    },
    {
        "name": "employee",
        "description": "Endpoints qui gèrent les employés."
    },
    {
        "name": "format",
        "description": "Endpoints qui gèrent les formats d'articles."
    },
    {
        "name": "genre",
        "description": "Endpoints qui gèrent les genres d'articles."
    },
    {
        "name": "item",
        "description": "Endpoints qui gèrent les articles."
    },
    {
        "name": "order_item",
        "description": "Endpoints qui gèrent les articles des commandes."
    },
    {
        "name": "orders",
        "description": "Endpoints qui gèrent les commandes."
    },
    {
        "name": "payment_method",
        "description": "Endpoints qui gèrent les méthodes de paiement."
    },
    {
        "name": "province",
        "description": "Endpoints qui gèrent les provinces."
    }
]

app = FastAPI(title="MusicaApp", description="Projet de développement d'une API REST.", version="1.0",
              contact={"Nom": "Samuel Legendre"}, openapi_tags=_tags_metadata)

app.include_router(customer.router)
app.include_router(employee.router)
app.include_router(format.router)
app.include_router(genre.router)
app.include_router(item.router)
app.include_router(order_item.router)
app.include_router(orders.router)
app.include_router(payment_method.router)
app.include_router(province.router)

app.mount("/musica", StaticFiles(directory="musica", html=True), name="musica")
