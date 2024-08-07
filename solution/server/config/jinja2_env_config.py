from fastapi import templating
from services.category_service import all, CATEGORIES_PAGE_SIZE
from services.product_service import PRODUCT_PAGE_SIZE
from services.users_service import is_authenticated
from math import ceil


class CustomJinja2Templates(templating.Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['all_categories'] = all
        self.env.globals['get_number_of_pages'] = get_number_of_pages
        self.env.globals['categories_page_size'] = CATEGORIES_PAGE_SIZE
        self.env.globals['get_current_page'] = get_current_page
        self.env.globals['products_page_size'] = PRODUCT_PAGE_SIZE
        self.env.globals['check_user'] = check_user



def get_number_of_pages(number_of_items: int, page_size: int) -> int:
    return ceil(number_of_items / page_size)

def get_current_page(path: str) -> int:
    path_str = str(path)
    page = 1
    if "page=" in path_str:
        page = int(path_str.split("=")[1])
    
    return page

def check_user(token: str):
    return is_authenticated(token) != None