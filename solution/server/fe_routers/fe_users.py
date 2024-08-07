from fastapi import APIRouter, Header, Request, Form, Response
from fastapi.responses import RedirectResponse
from common.auth import get_user_or_raise_401
from common.responses import BadRequest
from data.models import LoginData, Order, UserResponse
from services import users_service
from services import order_service
from config.jinja2_env_config import CustomJinja2Templates

fe_users_router = APIRouter(prefix='/users')
templates = CustomJinja2Templates(directory="templates")

@fe_users_router.get('/login')
def serve_login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')

@fe_users_router.post('/login')
def handle_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users_service.try_login(username, password)

    if user:
        token = users_service.create_token(user)
        response = RedirectResponse(url='/',status_code=302)
        response.set_cookie('token', token)
        return response
    else:
        return templates.TemplateResponse(request=request, name='login.html', context={'error': "Wrong username or password!"})
    
@fe_users_router.get('/register')
def serve_register(request: Request):
    return templates.TemplateResponse(request=request, name='register.html')

@fe_users_router.post('/register')
def handle_register(request: Request, username: str = Form(...), password: str = Form(...)):
    user = users_service.create(username, password)
    if user:
        response = RedirectResponse(url="/", status_code=302)
        token = users_service.create_token(user)
        response.set_cookie('token', token)
        return response
    return templates.TemplateResponse(request=request, name='register.html', context={"error": "Username already taken"})
    
@fe_users_router.post('/logout')
def logout(request: Request):
    response = RedirectResponse('/', status_code=302)
    response.delete_cookie('token')
    return response