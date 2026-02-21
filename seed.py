from __future__ import annotations

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db

from app.auth.models import User
from app.products.models import Product
from app.orders.models import Order, OrderLine


def get_or_create_user(*, email: str, password: str, first_name: str, last_name: str, role: str) -> User:
    email = email.strip().lower()
    user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
    if user:
        return user

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        role=role,
    )
    db.session.add(user)
    db.session.flush()
    return user


def get_or_create_product(**kwargs) -> Product:
    ean = kwargs["ean"]
    p = db.session.execute(db.select(Product).where(Product.ean == ean)).scalar_one_or_none()
    if p:
        return p

    p = Product(**kwargs)
    db.session.add(p)
    db.session.flush()
    return p


def set_if_exists(obj, field: str, value):
    if hasattr(obj, field):
        setattr(obj, field, value)


def create_order(
    *,
    user_id: int,
    shipping_address: str,
    items: list[tuple[Product, int]],
    status: str = "en_attente",
    created_at: datetime | None = None,
) -> Order:
    created_at = created_at or datetime.now(timezone.utc)

    order = Order(
        user_id=user_id,
        shipping_address=shipping_address,
    )
    set_if_exists(order, "created_at", created_at)
    set_if_exists(order, "status", status)

    total = 0.0
    for product, qty in items:
        unit_price = float(product.price)
        line = OrderLine(
            product_id=product.id,
            quantity=qty,
            unit_price=unit_price,
        )
        order.lines.append(line)
        total += unit_price * qty

    set_if_exists(order, "total_amount", total)

    db.session.add(order)
    db.session.flush()

    # Décrément stock si commande validée/expédiée
    if status in {"validee", "expediee"}:
        for product, qty in items:
            product.stock -= qty

    return order


def seed():
    # --- USERS ---
    admin = get_or_create_user(
        email="admin@digimarket.test",
        password="Admin123!",
        first_name="Admin",
        last_name="Digimarket",
        role="admin",
    )

    alice = get_or_create_user(
        email="alice@digimarket.test",
        password="Client123!",
        first_name="Alice",
        last_name="Martin",
        role="client",
    )
    bob = get_or_create_user(
        email="bob@digimarket.test",
        password="Client123!",
        first_name="Bob",
        last_name="Durand",
        role="client",
    )
    chris = get_or_create_user(
        email="chris@digimarket.test",
        password="Client123!",
        first_name="Chris",
        last_name="Bernard",
        role="client",
    )

    # --- PRODUCTS ---
    products_data = [
        dict(ean="3760000000001", brand="Logitech", name="Clavier mécanique", description="AZERTY rétroéclairé", category="informatique", price=89.99, stock=30),
        dict(ean="3760000000002", brand="Logitech", name="Souris sans fil", description="Ergonomique 1600 DPI", category="informatique", price=29.99, stock=50),
        dict(ean="3760000000003", brand="Dell", name="Laptop 15 pouces", description="i7 / 16Go / 512Go SSD", category="informatique", price=999.00, stock=10),
        dict(ean="3760000000004", brand="HP", name="Écran 24 pouces", description="Full HD IPS", category="informatique", price=159.90, stock=18),
        dict(ean="3760000000005", brand="Samsung", name="SSD NVMe 1To", description="Très haut débit", category="informatique", price=119.99, stock=25),
        dict(ean="3760000000006", brand="Seagate", name="HDD externe 2To", description="USB 3.0", category="informatique", price=79.99, stock=22),
        dict(ean="3760000000007", brand="Corsair", name="RAM 16Go DDR4", description="3200 MHz", category="informatique", price=74.99, stock=40),
        dict(ean="3760000000008", brand="TP-Link", name="Routeur WiFi AC1200", description="Double bande", category="informatique", price=59.99, stock=16),
        dict(ean="3760000000009", brand="Apple", name="MacBook Air M2", description="13 pouces", category="informatique", price=1299.00, stock=6),
        dict(ean="3760000000010", brand="Microsoft", name="Clavier Bluetooth", description="Ultra fin", category="informatique", price=99.99, stock=14),
    ]
    products = [get_or_create_product(**p) for p in products_data]

    by_name = {p.name: p for p in products}

    # --- ORDERS ---
    # Pour éviter les doublons d’orders, on seed seulement si la table est vide
    existing_orders = db.session.execute(db.select(Order).limit(1)).scalar_one_or_none()
    if existing_orders:
        print("Commandes déjà présentes -> seed orders ignoré (idempotent).")
        db.session.commit()
        return

    # Commande Alice: en attente (stock non décrémenté)
    create_order(
        user_id=alice.id,
        shipping_address="12 rue Exemple, 75001 Paris",
        items=[
            (by_name["Souris sans fil"], 1),
            (by_name["Clavier mécanique"], 1),
        ],
        status="en_attente",
    )

    # Commande Bob: validée (stock décrémenté)
    create_order(
        user_id=bob.id,
        shipping_address="3 avenue République, 69002 Lyon",
        items=[
            (by_name["Écran 24 pouces"], 1),
            (by_name["SSD NVMe 1To"], 1),
        ],
        status="validee",
    )

    # Commande Chris: expédiée (stock décrémenté)
    create_order(
        user_id=chris.id,
        shipping_address="8 boulevard des Tests, 13001 Marseille",
        items=[
            (by_name["Laptop 15 pouces"], 1),
            (by_name["Routeur WiFi AC1200"], 1),
        ],
        status="expediee",
    )

    # Petite commande admin (ex: commande interne / test)
    create_order(
        user_id=admin.id,
        shipping_address="HQ Digimarket, 75008 Paris",
        items=[
            (by_name["RAM 16Go DDR4"], 2),
        ],
        status="validee",
    )

    db.session.commit()
    print("✅ Seed complet terminé : users + produits + commandes.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()