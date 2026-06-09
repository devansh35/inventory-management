from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    quantity_in_stock: int

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    quantity_in_stock: int | None = None   

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    price: Decimal
    quantity_in_stock: int
    created_at: datetime
    updated_at: datetime