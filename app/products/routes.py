from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.auth.decorators import require_authentication, require_role
from app.products.models import Product
from app.products.validators import validate_product_creation, validate_product_update

products_bp = Blueprint("products", __name__)

# GET /api/produits?q=...&category=...
@products_bp.get("")
def list_products():
    q = (request.args.get("q") or "").strip()
    category = (request.args.get("category") or "").strip()

    stmt = db.select(Product)

    if category:
        stmt = stmt.where(Product.category == category)

    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                Product.name.ilike(like),
                Product.description.ilike(like),
                Product.category.ilike(like),
            )
        )

    products = db.session.execute(stmt).scalars().all()
    return jsonify([p.to_dict() for p in products]), 200


# GET /api/produits/<id>
@products_bp.get("/<int:product_id>")
def get_product(product_id: int):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Produit introuvable"}), 404
    return jsonify(product.to_dict()), 200


# POST /api/produits (admin only)
@products_bp.post("")
@require_authentication
@require_role("admin")
def create_product():
    data = request.get_json(silent=True) or {}

    errors = validate_product_creation(data)
    if errors:
        return jsonify({"errors": errors}), 400

    product = Product(
        name=data["name"].strip(),
        description=data["description"].strip(),
        category=data["category"].strip(),
        price=float(data["price"]),
        stock=int(data["stock"]),
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


# PUT /api/produits/<id> (admin only)
@products_bp.put("/<int:product_id>")
@require_authentication
@require_role("admin")
def update_product(product_id: int):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Produit introuvable"}), 404

    data = request.get_json(silent=True) or {}

    errors = validate_product_update(data)
    if errors:
        return jsonify({"errors": errors}), 400

    product.name = data["name"].strip()
    product.description = data["description"].strip()
    product.category = data["category"].strip()
    product.price = float(data["price"])
    product.stock = int(data["stock"])

    db.session.commit()
    return jsonify(product.to_dict()), 200


# DELETE /api/produits/<id> (admin only)
@products_bp.delete("/<int:product_id>")
@require_authentication
@require_role("admin")
def delete_product(product_id: int):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Produit introuvable"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Produit supprimé"}), 200
