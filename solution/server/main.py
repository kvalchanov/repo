from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.product import product_router
from routers.categories import categories_router
from routers.orders import orders_router
from routers.users import users_router
from fe_routers.fe_product import fe_product_router
from fe_routers.fe_index import fe_index_router
from fe_routers.fe_categories import fe_categories_router
from fe_routers.fe_users import fe_users_router
from jinja2 import Environment


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(fe_index_router)
app.include_router(fe_product_router)
app.include_router(fe_categories_router)
app.include_router(fe_users_router)
app.include_router(product_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(users_router)

