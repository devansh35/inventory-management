from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class CustomerCreate(BaseModel):
    full_name: str
    email: str
    phone_number: str

class CustomerUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone_number: str | None = None

class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: str
    phone_number: str
    created_at: datetime
    updated_at: datetime