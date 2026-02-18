from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, Numeric, UniqueConstraint

class Product(db.Model):
    __tablename__ = "products"

    # Contrainte d'unicité EAN (code barre)
    __table_args__ = (
        UniqueConstraint("ean", name="uq_products_ean"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ean: Mapped[str] = mapped_column(String(13), nullable=False, index=True)
    brand: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ean": self.ean,
            "name": self.name,
            "brand": self.brand,
            "description": self.description,
            "category": self.category,
            "price": float(self.price),
            "stock": self.stock,
            "available": self.stock > 0,
        }
