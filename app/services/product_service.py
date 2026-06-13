from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            quantity_in_stock=product_data.quantity_in_stock
        )

        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    async def get_product_by_id(self, db: AsyncSession, product_id: UUID) -> Product | None:
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_all_products(self, db: AsyncSession) -> list[Product]:
        result = await db.execute(select(Product))
        return result.scalars().all()

    async def update_product(self, db: AsyncSession, product_id: UUID, product_data: ProductUpdate) -> Product | None:
        product = await self.get_product_by_id(db, product_id)

        if not product:
            return None

        update_data = product_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        await db.commit()
        await db.refresh(product)
        return product

    async def delete_product(self, db: AsyncSession, product_id: UUID) -> bool:
        product = await self.get_product_by_id(db, product_id)

        if not product:
            return False

        await db.delete(product)
        await db.commit()
        return True    

product_service = ProductService()