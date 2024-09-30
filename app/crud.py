# Запросы в базу данных
from sqlalchemy import select, update, delete

from app.models import Product, Order, OrderItem
from app.schemas import ProductCreate
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async def create_product(product : ProductCreate,db : AsyncSession):
    product_model = Product(**product.dict())
    db.add(product_model)
    await db.commit()
    await db.refresh(product_model)
    return product_model

async def get_products(db, skip, limit):
    query = await db.execute(select(Product).offset(skip).limit(limit))
    return query.scalars().all()


async def get_product(db, id):
    product = await db.execute(select(Product).where(Product.id == id))
    return product.scalars().first()


async def update_product(db, id, product):
    await db.execute(update(Product).where(Product.id==id).values(**product.dict()))
    await db.commit()
    return await get_product(db,id)


async def delete_product(db, id):
    await db.execute(delete(Product).where(Product.id == id))
    await db.commit()
    return {"detail": "Product deleted"}


async def create_order(order, db):
    for item in order.items:
        product = await get_product(db, item.product_id)
        if not product:
            raise ValueError(f"Product with id {item.product_id} not found")
        if product.stock < item.quantity:
            raise ValueError(f"Not enough quantity of product {product.name} (available: {product.stock})")
    order_model = Order(date=order.date.replace(tzinfo=None), status=order.status)
    db.add(order_model)
    await db.commit()
    await db.refresh(order_model)
    for item in order.items:
        order_item_model = OrderItem(order_id = order_model.id, product_id=item.product_id, quantity=item.quantity)
        db.add(order_item_model)
        product = await get_product(db, item.product_id)
        product.stock -= item.quantity
    await db.commit()
    await db.refresh(order_model)
    return order_model

async def get_orders(db, skip, limit):
    query = await db.execute(select(Order).offset(skip).limit(limit))
    return query.scalars().all()


async def get_order(db, id):
    order = await db.execute(select(Order).where(Order.id == id))
    return order.scalars().first()


async def update_order(db, id, status):
    await db.execute(update(Order).where(Order.id==id).values(status=status))
    await db.commit()
    return await get_order(db,id)
