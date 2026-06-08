import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import OrderStatus
from app.models.mixins import UUIDMixin, TimestampMixin

class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "total_amount >= 0",
            name="ck_orders_total_amount_non_negative"
        ),
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")