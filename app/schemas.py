import datetime
from typing import List

from pydantic import BaseModel

from app.models import OrderStatus


class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    stock: int
class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int



class OrderBase(BaseModel):
    date: datetime.datetime
    status: OrderStatus
    items: List[OrderItemBase]

class Order(BaseModel):
    id: int
    date: datetime.datetime
    status: OrderStatus
    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    pass




