from datetime import date
from pydantic import BaseModel, constr


class Category(BaseModel):
    id: int | None
    name: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    @classmethod
    def from_query_result(cls, id, name):
        return cls(id=id, name=name)


class Product(BaseModel):
    id: int | None
    name: str
    description: str
    price: float
    category_id: int

    @classmethod
    def from_query_result(cls, id, name, description, price, category_id):
        return cls(
            id=id,
            name=name,
            description=description,
            price=price,
            category_id=category_id)


class Order(BaseModel):
    id: int | None
    product_ids: list[int] = []
    delivery_date: date
    delivery_address: str | None
    user_id: int | None

    @classmethod
    def from_query_result(cls, id, delivery_date, delivery_address, user_id=None, product_ids=[]):
        return cls(
            id=id,
            delivery_date=delivery_date,
            delivery_address=delivery_address,
            user_id=user_id,
            product_ids=product_ids)


class OrderUpdate(BaseModel):
    delivery_date: date
    delivery_address: str | None


class Role:
    CUSTOMER = 'customer'
    ADMIN = 'admin'


# TUsername = constr(regex='^\w{2,30}$')


class User(BaseModel):
    id: int | None
    username: str
    password: str
    role: str

    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id, username, password, role):
        return cls(
            id=id,
            username=username,
            password=password,
            role=role)


class LoginData(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class OrderResponse(BaseModel):
    id: int
    customer: UserResponse
    products: list[Product]
    delivery_date: date
    delivery_address: str | None
    order_total: float
