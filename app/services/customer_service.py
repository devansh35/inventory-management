from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import logger
from app.exceptions.customer import CustomerAlreadyExists, CustomerNotFound
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate

class CustomerService:
    async def create_customer(self, db: AsyncSession, customer_data: CustomerCreate) -> Customer:
        if await self.get_customer_by_email(db, customer_data.email):
            logger.warning(f"Customer with email {customer_data.email} already exists")
            raise CustomerAlreadyExists()

        customer = Customer(
            full_name=customer_data.full_name,
            email=customer_data.email,
            phone_number=customer_data.phone_number
        )

        db.add(customer)
        await db.commit()
        await db.refresh(customer)

        logger.info(f"Customer {customer.id} created successfully")
        return customer

    async def get_customer_by_id(self, db: AsyncSession, customer_id: UUID) -> Customer:
        result = await db.execute(select(Customer).where(Customer.id == customer_id))
        customer = result.scalar_one_or_none()

        if not customer:
            logger.warning(f"Customer with id {customer_id} not found")
            raise CustomerNotFound()

        return customer

    async def get_all_customers(self, db: AsyncSession) -> list[Customer]:
        result = await db.execute(select(Customer))
        return result.scalars().all()        

    async def update_customer(self, db: AsyncSession, customer_id: UUID, customer_data: CustomerUpdate) -> Customer:
        customer = await self.get_customer_by_id(db, customer_id)

        if customer_data.email:
            existing_customer = await self.get_customer_by_email(db, customer_data.email)
            
            if existing_customer and existing_customer.id != customer.id:
                logger.warning(f"Customer with email {customer_data.email} already exists")
                raise CustomerAlreadyExists()
        
        update_data = customer_data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(customer, key, value)
        
        await db.commit()
        await db.refresh(customer)
        
        logger.info(f"Customer {customer.id} updated successfully")
        return customer

    async def delete_customer(self, db: AsyncSession, customer_id: UUID) -> None:
        customer = await self.get_customer_by_id(db, customer_id)

        await db.delete(customer)
        await db.commit()

        logger.info(f"Customer {customer.id} deleted successfully")

    async def get_customer_by_email(self, db: AsyncSession, email: str) -> Customer | None:
        result = await db.execute(select(Customer).where(Customer.email == email))
        return result.scalar_one_or_none()

customer_service = CustomerService()