from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from common.responses import BadRequest, NotFound
from data.models import Product
from services import product_service
from services import category_service
from config.jinja2_env_config import CustomJinja2Templates


fe_index_router = APIRouter(prefix='')
templates = CustomJinja2Templates(directory="templates")

@fe_index_router.get('/', response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")