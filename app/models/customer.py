from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import UUIDMixin, TimestampMixin

class Customer(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "customers"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(30), nullable=False)
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")