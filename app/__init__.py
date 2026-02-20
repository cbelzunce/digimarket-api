from http.client import HTTPException
from flask import Flask, jsonify
from app.extensions import db
from app.cli import register_cli


"""
Pour passer en mode Tests
create_app({
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite://",
})
"""
def create_app(config_overrides: dict | None = None):
    app = Flask(__name__)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///project.db",
        TESTING=False,
        JWT_SECRET="dev-secret-change-me",
        JWT_EXPIRES_MINUTES=60,
    )

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

     # Importer les modèles ORM
    from app.auth.models import User
    from app.products.models import Product
    from app.orders.models import Order, OrderLine

    # Créer les tables
    with app.app_context():
        db.create_all()

    # Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.products.routes import products_bp
    app.register_blueprint(products_bp, url_prefix="/api/produits")

    from app.orders.routes import orders_bp
    app.register_blueprint(orders_bp, url_prefix="/api/commandes")

    # Enregistrer les commandes cli (ex: crea admin)
    register_cli(app)

    '''
    # Optionnel : sécurité pour éviter de renvoyer du HTML en prod
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        return jsonify({"message": "Internal server error"}), 500
    '''
    return app
