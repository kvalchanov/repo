from fastapi import APIRouter, Header
from common.responses import BadRequest, InternalServerError, NoContent, NotFound, Unauthorized
from common.auth import get_user_or_raise_401
from data.models import Order, OrderResponse, OrderUpdate
from services import order_service
from services import product_service
from services import users_service


orders_router = APIRouter(prefix='/orders')


@orders_router.get('/')
def get_orders(sort: str | None = None, x_token=Header()):
    user = get_user_or_raise_401(x_token)
    if not user.is_admin():
        return Unauthorized('Admin endpoint')

    orders = order_service.all()

    if sort and (sort == 'asc' or sort == 'desc'):
        return order_service.sort(orders, reverse=sort == 'desc')
    else:
        return orders


@orders_router.get('/{id}', response_model=OrderResponse)
def get_order_by_id(id: int, x_token: str = Header()):
    customer = get_user_or_raise_401(x_token)
    order = order_service.get_by_id(id)
    if not order or not users_service.owns_order(customer, order):
        return NotFound()

    products = order_service.get_order_products(order.id)

    return order_service.create_response_object(
        customer,
        order,
        products)


@orders_router.post('/', response_model=OrderResponse)
def create_order(order: Order, x_token: str = Header()):
    customer = get_user_or_raise_401(x_token)

    if order.product_ids == []:
        return BadRequest('Must contain at least one product')

    products = product_service.get_many(order.product_ids)

    if len(products) < len(order.product_ids):
        return BadRequest('Must contain existing products')

    order = order_service.create(order, customer)

    return order_service.create_response_object(customer, order, products)


@orders_router.put('/{id}')
def update_order(id: int, data: OrderUpdate, x_token: str = Header()):
    customer = get_user_or_raise_401(x_token)

    order = order_service.get_by_id(id)
    if order is None:
        return NotFound()

    if not users_service.owns_order(customer, order):
        return Unauthorized('Can`t edit others` orders')

    order = order_service.update(data, order)

    # we don't know what to return if the order is not successfully updated
    return order or InternalServerError()


@orders_router.put('/{order_id}/products')
def add_products(order_id: int, product_ids: set[int], x_token: str = Header()):
    customer = get_user_or_raise_401(x_token)
    order = order_service.get_by_id(order_id)
    if order is None:
        return NotFound()
    if not users_service.owns_order(customer, order):
        return Unauthorized('Can`t edit others` orders')

    current_ids = order_service.get_ordered_product_ids(order_id)
    products_to_add = product_ids.difference(current_ids)

    if len(products_to_add) == 0:
        return {'added_product_ids': []}

    order_service.insert_products_to_order(order_id, products_to_add)

    return {'added_product_ids': products_to_add}


@orders_router.delete('/{order_id}/products')
def remove_products(order_id: int, product_ids: set[int], x_token: str = Header()):
    customer = get_user_or_raise_401(x_token)
    order = order_service.get_by_id(order_id)
    if order is None:
        return NotFound()
    if not users_service.owns_order(customer, order):
        return Unauthorized('Can`t edit others` orders')

    current_ids = order_service.get_ordered_product_ids(order_id)
    products_to_delete = product_ids.intersection(current_ids)
    if len(products_to_delete) == 0:
        return {'deleted_product_ids': []}

    order_service.remove_products_from_order(order_id, products_to_delete)

    return {'deleted_product_ids': products_to_delete}


@orders_router.delete('/{id}')
def delete_order(id: int, x_token: str = Header()):
    customer = get_user_or_raise_401(x_token)
    order = order_service.get_by_id(id)
    if order is None:
        return NotFound()

    if not users_service.owns_order(customer, order):
        return Unauthorized('Can`t delete others` orders')

    order_service.delete(order)

    return NoContent()
