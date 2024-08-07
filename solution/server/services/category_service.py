from data.database import insert_query, read_query
from data.models import Category

CATEGORIES_PAGE_SIZE = 6

def all(page: int = 1):
    starting_index = (page * CATEGORIES_PAGE_SIZE) - CATEGORIES_PAGE_SIZE
    data = read_query('select id, name from categories')

    return (Category.from_query_result(*row) for row in data)


def get_by_id(id: int):
    data = read_query('select id, name from categories where id = ?', (id,))

    return next((Category(id=id, name=name) for id, name in data), None)


def exists(id: int):
    return any(
        read_query(
            'select id, name from categories where id = ?',
            (id,)))


def create(category: Category):
    generated_id = insert_query(
        'insert into categories(name) values(?)',
        (category.name,))

    category.id = generated_id

    return category

def count_categories() -> int: 
    count = read_query('select count(*) from categories')
    return int(count[0][0])