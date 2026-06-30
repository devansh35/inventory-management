from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    phone_number: str = Field(..., min_length=1)

class CustomerUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1)
    email: str | None = Field(None, min_length=1)
    phone_number: str | None = Field(None, min_length=1)

class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    full_name: str
    email: str
    phone_number: str
    created_at: datetime
    updated_at: datetime