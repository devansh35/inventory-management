from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.customer_service import customer_service

router = APIRouter()

@router.post("/customers", response_model=CustomerResponse, status_code=201)
async def create_customer(customer_data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    return await customer_service.create_customer(db, customer_data)

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer_by_id(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    return await customer_service.get_customer_by_id(db, customer_id)

@router.get("/customers", response_model=list[CustomerResponse])
async def get_all_customers(db: AsyncSession = Depends(get_db)):
    return await customer_service.get_all_customers(db)

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: UUID, customer_data: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    return await customer_service.update_customer(db, customer_id, customer_data)

@router.delete("/customers/{customer_id}", status_code=204)
async def delete_customer(customer_id: UUID, db: AsyncSession = Depends(get_db)):
    await customer_service.delete_customer(db, customer_id)