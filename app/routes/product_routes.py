from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import product_service

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product_data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await product_service.create_product(db, product_data)

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: UUID, db: AsyncSession = Depends(get_db)):
    return await product_service.get_product_by_id(db, product_id)

@router.get("/products", response_model=list[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    return await product_service.get_all_products(db)

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: UUID, product_data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await product_service.update_product(db, product_id, product_data)

@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    await product_service.delete_product(db, product_id)