from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from common.responses import BadRequest, NotFound
from data.models import Product
from services import product_service
from services import category_service
from config.jinja2_env_config import CustomJinja2Templates

fe_categories_router = APIRouter(prefix='/categories')
templates = CustomJinja2Templates(directory="templates")

@fe_categories_router.get('', response_class=HTMLResponse)
def get_categories(request: Request, page: int = 1):
    categories = list(category_service.all(page))
    total_number_of_categories = category_service.count_categories()
    return templates.TemplateResponse(request=request, name="categories.html", 
                                      context={"categories": categories, "page": page, "number_of_categories": total_number_of_categories})

@fe_categories_router.get('/{id}')
def get_category_by_id(request: Request, id: int):
    category = category_service.get_by_id(id)
    products = list(product_service.get_by_category(category.id))
    print(products)
    return templates.TemplateResponse(request=request, name="single-category.html", context={"category": category, "products": products})