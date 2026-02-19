from flask import Blueprint, request, jsonify, g
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from app.extensions import db
from app.auth.decorators import require_authentication, require_role
from app.orders.models import Order, OrderLine
from app.orders.validators import validate_order_creation, validate_status_patch
from app.products.models import Product

orders_bp = Blueprint("orders", __name__)

def _current_user_id() -> int:
    # payload.sub est une string (souvent)
    return int(g.user["sub"])

# TODO: un seul role possible, du coup modif (ou garder pour évol ??)
def _is_admin() -> bool:
    roles = g.user.get("roles", [])
    return "admin" in roles


@orders_bp.get("")
@require_authentication
def list_orders():
    user_id = _current_user_id()

    stmt = select(Order).order_by(Order.created_at.desc())

    if not _is_admin():
        stmt = stmt.where(Order.user_id == user_id)

    orders = db.session.execute(stmt).scalars().all()
    return jsonify([o.to_dict() for o in orders]), 200


@orders_bp.get("/<int:order_id>")
@require_authentication
def get_order(order_id: int):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Commande introuvable"}), 404

    # client ne voit que ses commandes
    if not _is_admin() and order.user_id != _current_user_id():
        return jsonify({"message": "Accès interdit"}), 403

    return jsonify(order.to_dict()), 200


@orders_bp.get("/<int:order_id>/lignes")
@require_authentication
def get_order_lines(order_id: int):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Commande introuvable"}), 404

    if not _is_admin() and order.user_id != _current_user_id():
        return jsonify({"message": "Accès interdit"}), 403

    return jsonify([l.to_dict() for l in order.lines]), 200


@orders_bp.post("")
@require_authentication
def create_order():
    data = request.get_json(silent=True) or {}
    erreurs = validate_order_creation(data)
    if erreurs:
        return jsonify({"errors": erreurs}), 400

    user_id = _current_user_id()
    items = data["items"]
    shipping_address = data["shipping_address"].strip()

    # 1) Charger les produits demandés
    product_ids = [int(it["product_id"]) for it in items]
    products = db.session.execute(
        select(Product).where(Product.id.in_(product_ids))
    ).scalars().all()

    products_by_id = {p.id: p for p in products}

    # 2) Vérifier que tous les produits existent
    missing = [pid for pid in product_ids if pid not in products_by_id]
    if missing:
        return jsonify({"errors": {"items": f"Produits introuvables: {missing}"}}), 400

    # 3) Vérifier le stock (mais on ne décrémente pas ici : décrément à validation)
    insufficient = []
    for it in items:
        pid = int(it["product_id"])
        qty = int(it["quantity"])
        p = products_by_id[pid]
        if p.stock < qty:
            insufficient.append({"product_id": pid, "stock": p.stock, "requested": qty})

    if insufficient:
        return jsonify({"errors": {"stock": insufficient}}), 409

    # 4) Construire la commande + lignes + total
    order = Order(
        user_id=user_id,
        status="en_attente",
        shipping_address=shipping_address,
        total_amount=0,
    )

    total = 0.0
    for it in items:
        pid = int(it["product_id"])
        qty = int(it["quantity"])
        p = products_by_id[pid]

        unit_price = float(p.price)
        total += unit_price * qty

        order.lines.append(
            OrderLine(product_id=pid, quantity=qty, unit_price=unit_price)
        )

    order.total_amount = total

    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict()), 201


@orders_bp.patch("/<int:order_id>")
@require_authentication
@require_role("admin")
def patch_order_status(order_id: int):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Commande introuvable"}), 404

    data = request.get_json(silent=True) or {}
    erreurs = validate_status_patch(data)
    if erreurs:
        return jsonify({"errors": erreurs}), 400

    new_status = data["status"].strip()

    # logique simple de transition
    old_status = order.status
    order.status = new_status

    # Décrément stock uniquement au passage vers "validee"
    if old_status != "validee" and new_status == "validee":
        # On re-vérifie et on décrémente de façon transactionnelle
        try:
            for line in order.lines:
                product = db.session.get(Product, line.product_id)
                if not product:
                    return jsonify({"message": "Produit introuvable dans une ligne"}), 400

                if product.stock < line.quantity:
                    db.session.rollback()
                    return jsonify({
                        "errors": {"stock": f"Stock insuffisant pour product_id={product.id}"}
                    }), 409

                product.stock -= line.quantity

            db.session.commit()
        except OperationalError as e:
            db.session.rollback()
            return jsonify({"message": "Base de données verrouillée, réessayez."}), 503

        return jsonify(order.to_dict()), 200

    db.session.commit()
    return jsonify(order.to_dict()), 200
