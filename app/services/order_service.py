from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import logger
from app.exceptions.order import OrderNotFound, InsufficientStock
from app.exceptions.product import ProductNotFound
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate
from app.services.customer_service import customer_service
from app.services.product_service import product_service

class OrderService:
    async def create_order(self, db: AsyncSession, order_data: OrderCreate) -> Order:
        async with db.begin():
            await customer_service.get_customer_by_id(db, order_data.customer_id)

            product_ids = list({item.product_id for item in order_data.items})
            products = await product_service.get_products_by_ids(db, product_ids)

            total_amount = Decimal("0.00")

            for item in order_data.items:
                product = products.get(item.product_id)

                if not product:
                    logger.warning(f"Product with id {item.product_id} not found")
                    raise ProductNotFound()

                if item.quantity > product.quantity_in_stock:
                    logger.warning(f"Insufficient stock for product {product.id}")
                    raise InsufficientStock()

                total_amount += product.price * item.quantity

            order = Order(
                customer_id=order_data.customer_id,
                total_amount=total_amount
            )

            db.add(order)
            await db.flush()

            for item in order_data.items:
                product = products[item.product_id]

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                    subtotal=product.price * item.quantity                    
                )

                db.add(order_item)
                product.quantity_in_stock -= item.quantity

        logger.info(f"Order {order.id} created successfully")
        
        result = await db.execute(select(Order).options(selectinload(Order.items)).where(Order.id == order.id))
        return result.scalar_one()

    async def get_order_by_id(self, db: AsyncSession, order_id: UUID) -> Order:
        result = await db.execute(select(Order).options(selectinload(Order.items)).where(Order.id == order_id))
        order = result.scalar_one_or_none()

        if not order:
            logger.warning(f"Order with id {order_id} not found")
            raise OrderNotFound()

        return order

    async def get_all_orders(self, db: AsyncSession) -> list[Order]:
        result = await db.execute(select(Order).options(selectinload(Order.items)).order_by(Order.created_at.desc()))
        return result.scalars().all()

    async def delete_order(self, db: AsyncSession, order_id: UUID) -> None:
        async with db.begin():
            order = await self.get_order_by_id(db, order_id)

            product_ids = list({item.product_id for item in order.items})
            products = await product_service.get_products_by_ids(db, product_ids)

            for item in order.items:
                product = products[item.product_id]
                product.quantity_in_stock += item.quantity

            await db.delete(order)

        logger.info(f"Order {order_id} deleted successfully")        

order_service = OrderService()