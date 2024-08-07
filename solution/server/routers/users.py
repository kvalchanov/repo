from fastapi import APIRouter, Header
from common.auth import get_user_or_raise_401
from common.responses import BadRequest
from data.models import LoginData, Order, UserResponse
from services import users_service
from services import order_service


users_router = APIRouter(prefix='/api/users')


@users_router.post('/login')
def login(data: LoginData):
    user = users_service.try_login(data.username, data.password)

    if user:
        token = users_service.create_token(user)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')


@users_router.get('/info')
def user_info(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    return UserResponse(id=user.id, username=user.username)


@users_router.get('/orders', response_model=list[Order])
def user_info(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    return order_service.get_user_orders(user)


@users_router.post('/register')
def register(data: LoginData):
    user = users_service.create(data.username, data.password)

    return user or BadRequest(f'Username {data.username} is taken.')
