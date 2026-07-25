from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import logger
from app.exceptions.product import ProductAlreadyExists, ProductNotFound
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        if await self.get_product_by_description(db, product_data.description):
            logger.warning(f"Product with description {product_data.description} already exists")
            raise ProductAlreadyExists()

        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            quantity_in_stock=product_data.quantity_in_stock
        )

        db.add(product)
        await db.commit()
        await db.refresh(product)

        logger.info(f"Product {product.id} created successfully")
        return product

    async def get_product_by_id(self, db: AsyncSession, product_id: UUID) -> Product:
        result = await db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()

        if not product:
            logger.warning(f"Product with id {product_id} not found")
            raise ProductNotFound()

        return product

    async def get_all_products(self, db: AsyncSession) -> list[Product]:
        result = await db.execute(select(Product))
        return result.scalars().all()

    async def update_product(self, db: AsyncSession, product_id: UUID, product_data: ProductUpdate) -> Product:
        product = await self.get_product_by_id(db, product_id)

        if product_data.description:
            existing_product = await self.get_product_by_description(db, product_data.description)
            
            if existing_product and existing_product.id != product.id:
                logger.warning(f"Product with description {product_data.description} already exists")
                raise ProductAlreadyExists()
        
        update_data = product_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        await db.commit()
        await db.refresh(product)

        logger.info(f"Product {product.id} updated successfully")
        return product

    async def delete_product(self, db: AsyncSession, product_id: UUID) -> None:
        product = await self.get_product_by_id(db, product_id)

        await db.delete(product)
        await db.commit()

        logger.info(f"Product {product.id} deleted successfully")   

    async def get_product_by_description(self, db: AsyncSession, description: str) -> Product | None:
        result = await db.execute(select(Product).where(Product.description == description))
        return result.scalar_one_or_none()

    async def get_products_by_ids(self, db: AsyncSession, product_ids: list[UUID]) -> dict[UUID, Product]:
        result = await db.execute(select(Product).where(Product.id.in_(product_ids)))
        products = result.scalars().all()    
        return {product.id: product for product in products}

product_service = ProductService()