from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    shipping_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    lines: Mapped[list["OrderLine"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="en_attente", index=True)

    __table_args__ = (
        CheckConstraint(
            "status IN ('en_attente','validee','expediee','annulee')",
            name="ck_orders_status",
        ),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "shipping_address": self.shipping_address,
            "created_at": self.created_at.isoformat(),
            "total_amount": float(self.total_amount),
        }


class OrderLine(db.Model):
    __tablename__ = "order_lines"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="lines")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_lines_quantity"),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
        }