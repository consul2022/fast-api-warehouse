from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.schemas import ProductCreate

router = APIRouter()


@router.post("/products", response_model=schemas.Product, tags=["products"])
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_product(product, db)


@router.get("/products", response_model=List[schemas.Product], tags=["products"])
async def read_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    products = await crud.get_products(db, skip=skip, limit=limit)
    return products


@router.get('/products/{id}', response_model=schemas.Product, tags=["products"])
async def read_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put('/products/{id}', response_model=schemas.Product, tags=["products"])
async def update_product(id: int, new_product: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = await crud.update_product(db, id=id, product=new_product)
    return updated_product


@router.delete('/products/{id}', response_model=schemas.Product, tags=["products"])
async def delete_product(id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await crud.delete_product(db, id=id)
    return product
