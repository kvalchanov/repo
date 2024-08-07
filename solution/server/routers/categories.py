from fastapi import APIRouter
from pydantic import BaseModel
from common.responses import NotFound
from data.models import Category, Product
from services import product_service
from services import category_service


class CategoryResponseModel(BaseModel):
    category: Category
    products: list[Product]


categories_router = APIRouter(prefix='/api/categories')


@categories_router.get('/')
def get_categories():
    return [
        CategoryResponseModel(
            category=category,
            products=product_service.get_by_category(category.id))  # known (n+1) problem
        for category in category_service.all()]


@categories_router.get('/{id}')
def get_category_by_id(id: int):
    category = category_service.get_by_id(id)

    if category is None:
        return NotFound()
    else:
        return CategoryResponseModel(
            category=category,
            products=product_service.get_by_category(category.id))


@categories_router.post('/')
def create_category(category: Category):
    created_category = category_service.create(category)

    return CategoryResponseModel(category=created_category, products=[])
