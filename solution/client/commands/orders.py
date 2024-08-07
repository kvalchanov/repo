import requests
from commands.action import Action
from config import BASE_URL
from views import order_response_view

ORDERS_URL = f'{BASE_URL}/orders'


def show_all(token):
    response = requests.get(f'{ORDERS_URL}', headers={'x-token': token})

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)


def single(token):
    order_id = int(input('Order id = '))
    response = requests.get(f'{ORDERS_URL}/{order_id}',
                            headers={'x-token': token})

    if response.status_code == 200:
        print(order_response_view(response.json()))
    elif response.status_code == 404:
        print('Order not found')
    else:
        print(response.text)


def create(token):
    delivery_date = input('To be delivered on (yyyy-MM-dd) = ')
    address = input('Address = ')
    product_ids = input('Product ids, separated by space = ')

    data = {
        'product_ids': [int(id) for id in product_ids.split()],
        'delivery_date': delivery_date,
        'delivery_address': address,
    }

    response = requests.post(f'{ORDERS_URL}',
                             headers={'x-token': token},
                             json=data)

    if response.status_code == 200:
        print(order_response_view(response.json()))
    else:
        print(response.text)


def update(token):
    order_id = int(input('Order id to update = '))
    delivery_date = input('New date (yyyy-MM-dd) = ')
    address = input('New address = ')

    data = {
        'delivery_date': delivery_date,
        'delivery_address': address,
    }

    response = requests.put(f'{ORDERS_URL}/{order_id}',
                            headers={'x-token': token},
                            json=data)

    if response.status_code == 200:
        print('Successfully updated.')
    else:
        print(response.text)


def delete(token):
    order_id = int(input('Order id to delete = '))
    response = requests.delete(f'{ORDERS_URL}/{order_id}',
                               headers={'x-token': token})

    if response.status_code == 204:
        print('Successfully deleted.')
    else:
        print(response.text)


def add_products(token):
    order_id = int(input('Order id to update = '))
    product_ids = input('Product ids to add, separated by space = ')

    response = requests.put(f'{ORDERS_URL}/{order_id}/products',
                            headers={'x-token': token},
                            json=[int(id) for id in product_ids.split()])

    if response.status_code == 200:
        print('Added product ids: ', end='')
        print(response.json()['added_product_ids'])
    else:
        print(response.text)


def remove_products(token):
    order_id = int(input('Order id to update = '))
    product_ids = input('Product ids to remove, separated by space = ')

    response = requests.delete(f'{ORDERS_URL}/{order_id}/products',
                               headers={'x-token': token},
                               json=[int(id) for id in product_ids.split()])

    if response.status_code == 200:
        print('Removed product ids: ', end='')
        print(response.json()['deleted_product_ids'])
    else:
        print(response.text)


def select_action():
    actions = {
        'A': Action(show_all, requires_login=True, name='[A]ll'),
        'S': Action(single, requires_login=True, name='[S]ingle'),
        'C': Action(create, requires_login=True, name='[C]reate'),
        'U': Action(update, requires_login=True, name='[U]pdate'),
        'D': Action(delete, requires_login=True, name='[D]elete'),
        'ADD': Action(add_products, requires_login=True, name='[ADD] Products'),
        'REM': Action(remove_products, requires_login=True, name='[REM]ove Products'),
    }

    print('Select orders action?')
    print(' / '.join(action.name for action in actions.values()))

    selected_action = input().upper()
    actions.get(selected_action, Action.default()).execute()
