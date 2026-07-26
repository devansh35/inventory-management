from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import order_service

router = APIRouter()


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await order_service.create_order(db, order_data)

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order_by_id(order_id: UUID, db: AsyncSession = Depends(get_db)):
    return await order_service.get_order_by_id(db, order_id)

@router.get("/orders", response_model=list[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    return await order_service.get_all_orders(db)

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    await order_service.delete_order(db, order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)