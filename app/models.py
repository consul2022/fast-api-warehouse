from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class OrderStatus(str, Enum):
    IN_PROGRESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    stock = Column(Integer)

    orders = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    status = Column(SQLEnum(OrderStatus))

    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="orders")








