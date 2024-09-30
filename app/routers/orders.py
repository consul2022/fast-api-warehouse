from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.database import get_db
from app.models import OrderStatus
from app.schemas import OrderCreate

router = APIRouter()


@router.post("/orders", response_model=schemas.Order, tags=["orders"])
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_order(order, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders", response_model=List[schemas.Order], tags=["orders"])
async def read_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    orders = await crud.get_orders(db, skip, limit)
    return orders


@router.get('/orders/{id}', response_model=schemas.Order, tags=["orders"])
async def read_order(id: int, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch('/orders/{id}/status', response_model=schemas.Order, tags=["orders"])
async def update_order(id: int, status: OrderStatus, db: AsyncSession = Depends(get_db)):
    order = await crud.get_order(db, id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    updated_order = await crud.update_order(db, id, status=status)
    return updated_order
