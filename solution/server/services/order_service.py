from data.database import insert_query, read_query, update_query
from data.models import Order, OrderResponse, OrderUpdate, Product, User, UserResponse


def get_by_id(order_id: int):
    order_data = read_query(
        'select id, delivery_date, delivery_address, user_id from orders where id = ?', (order_id,))

    return next((Order.from_query_result(*row) for row in order_data), None)


def all():
    data = read_query('''SELECT id, delivery_date, delivery_address, user_id, product_id
                         FROM orders AS o
                           LEFT JOIN orders_products AS op
                             ON o.id = op.order_id''')

    flattened_data = _flatten_order_products(data)

    return (Order.from_query_result(*obj) for obj in flattened_data.values())


def sort(lst: list[Order], reverse=False):
    return sorted(
        lst,
        key=lambda p: p.delivery_date,
        reverse=reverse)


def get_order_products(order_id: int) -> list[Product]:
    data = read_query(
        '''SELECT p.id, p.name, p.description, p.price, p.category_id
                FROM products p
                WHERE p.id in (SELECT product_id
                                FROM orders_products
                                WHERE order_id = ?)''',
        (order_id,))

    return [Product.from_query_result(*row) for row in data]


def get_user_orders(user: User):
    data = read_query('''SELECT id, delivery_date, delivery_address, user_id, product_id
                         FROM orders AS o
                           LEFT JOIN orders_products AS op
                             ON o.id = op.order_id
                         WHERE user_id = ?''', (user.id,))

    flattened_data = _flatten_order_products(data)

    return (Order.from_query_result(*obj) for obj in flattened_data.values())


def create(order: Order, customer: User):
    generated_id = insert_query(
        'INSERT INTO orders(delivery_date,delivery_address,user_id) VALUES(?,?,?)',
        (order.delivery_date, order.delivery_address, customer.id))

    order.id = generated_id

    insert_products_to_order(order.id, order.product_ids)

    return order


def exists(order_id: int):
    data = read_query('SELECT 1 from orders where id = ?', (order_id,))

    return any(data)


def get_ordered_product_ids(order_id: int) -> set[int]:
    data = read_query(
        'SELECT product_id from orders_products where order_id = ?', (order_id,))

    return set(i[0] for i in data)


def update(order_update: OrderUpdate, order: Order):
    result = update_query(
        '''UPDATE orders SET
           delivery_date = ?, delivery_address = ?
           WHERE id = ?''',
        (order_update.delivery_date, order_update.delivery_address, order.id))

    if result > 0:
        order.delivery_address = order_update.delivery_address
        order.delivery_date = order_update.delivery_date
        return order
    else:
        return None


def delete(order: Order):
    update_query('DELETE FROM orders_products WHERE order_id = ?', (order.id,))
    update_query('DELETE FROM orders WHERE id = ?', (order.id,))


def insert_products_to_order(order_id: int, product_ids: list[int]):
    relations = ','.join(
        f'({order_id},{product_id})' for product_id in product_ids)

    insert_query(
        f'INSERT INTO orders_products(order_id, product_id) VALUES {relations}')


def remove_products_from_order(order_id: int, product_ids: list[int]):
    ids_to_delete = ','.join(str(p_id) for p_id in product_ids)

    insert_query(
        f'''DELETE FROM orders_products
            WHERE order_id = ? and product_id IN ({ids_to_delete})''',
        (order_id,))


def create_response_object(customer: User, order: Order, order_products: list[Product]):
    FREE_SHIPPING_LIMIT = 125.0
    SHIPPING_FEE = 1.02

    order_total = sum(p.price for p in order_products)
    if order_total > FREE_SHIPPING_LIMIT:
        order_total = order_total * SHIPPING_FEE

    # changed to model for better http://127.0.0.1:8000/docs
    return OrderResponse(
        id=order.id,
        customer=UserResponse(id=customer.id, username=customer.username),
        products=order_products,
        delivery_date=order.delivery_date,
        delivery_address=order.delivery_address,
        order_total=round(order_total, 2))


def _flatten_order_products(data: list[tuple]):
    flattened = {}
    for id, delivery_date, delivery_address, user_id, product_id in data:
        if id not in flattened:
            flattened[id] = (id, delivery_date, delivery_address, user_id, [])

        if product_id is not None:
            flattened[id][-1].append(product_id)

    return flattened
