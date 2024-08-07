from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from common.responses import BadRequest, NotFound
from data.models import Product
from services import product_service
from services import category_service
from jinja2 import Environment
from config.jinja2_env_config import CustomJinja2Templates
from services.users_service import is_authenticated

fe_product_router = APIRouter(prefix='/products')
templates = CustomJinja2Templates(directory="templates")


@fe_product_router.get('', response_class=HTMLResponse)
def get_products(request: Request, page: int = 1):
    result = list(product_service.all(page=page))
    total_number_of_products = product_service.count_products()
    if is_authenticated(request.cookies.get('token')):
        return templates.TemplateResponse(request=request, 
                                      name="products.html", 
                                      context={"products": result, "page": page, "number_of_products": total_number_of_products})
    else:
        response = Response(status_code=302, headers={'location': '/'})
        return response

@fe_product_router.get('/{id}', response_class=HTMLResponse)
def get_product_by_id(request: Request, id: int):
    product = product_service.get_by_id(id)

    if product is None:
        return templates.TemplateResponse(request=request, name="not-found.html", context={"id": id})
    else:
        return templates.TemplateResponse(request=request, name="single-product.html", context={"product": product})
