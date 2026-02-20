from werkzeug.security import generate_password_hash
from app.extensions import db
from app.auth.models import User
from app.products.models import Product

def _make_admin_and_get_token(client, app, email="admin@example.com", password="MotDePasseSolide123!"):
    # 1) register via API
    r = client.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "first_name": "Admin",
        "last_name": "Test",
    })
    assert r.status_code == 201

    # 2) upgrade role to admin in DB
    with app.app_context():
        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one()
        user.role = "admin"
        db.session.commit()

    # 3) login via API -> token
    r = client.post("/api/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    return r.get_json()["access_token"]


def _create_product(app, *, ean, brand, name, stock, price=35.0, category="accessoires"):
    with app.app_context():
        p = Product(
            ean=ean,
            brand=brand,
            name=name,
            description="Test product",
            category=category,
            price=price,
            stock=stock,
        )
        db.session.add(p)
        db.session.commit()
        return p.id  # on retourne l'id (FK order_lines.product_id)


def test_admin_can_create_order(client, app):
    token = _make_admin_and_get_token(client, app)

    # Produits existants
    pid1 = _create_product(app, ean="3760123456789", brand="Logitech", name="Clavier", stock=10, price=35.0)
    pid2 = _create_product(app, ean="3760123456796", brand="Logitech", name="Souris", stock=5, price=20.0)

    # Création de commande
    r = client.post(
        "/api/commandes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "shipping_address": "12 rue de la République, 75000 Paris",
            "items": [
                {"product_id": pid1, "quantity": 2},  # 2 * 35 = 70
                {"product_id": pid2, "quantity": 1},  # 1 * 20 = 20
            ],
        },
    )

    assert r.status_code == 201
    data = r.get_json()

    assert data["status"] == "en_attente"
    assert data["shipping_address"] == "12 rue de la République, 75000 Paris"
    assert float(data["total_amount"]) == 90.0  # 70 + 20

    order_id = data["id"]

    # Vérifier les lignes via endpoint dédié
    r_lines = client.get(
        f"/api/commandes/{order_id}/lignes",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r_lines.status_code == 200
    lines = r_lines.get_json()
    assert len(lines) == 2

    # Stock non décrémenté à la création
    with app.app_context():
        p1 = db.session.get(Product, pid1)
        p2 = db.session.get(Product, pid2)
        assert p1.stock == 10
        assert p2.stock == 5


def test_create_order_stock_insufficient_returns_409(client, app):
    token = _make_admin_and_get_token(client, app)

    pid = _create_product(app, ean="3760123456802", brand="X", name="ProduitStockFaible", stock=1, price=10.0)

    r = client.post(
        "/api/commandes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "shipping_address": "12 rue de la République, 75000 Paris",
            "items": [{"product_id": pid, "quantity": 2}],  # demande > stock
        },
    )

    assert r.status_code == 409
    data = r.get_json()
    assert "errors" in data

