from http.client import HTTPException
from flask import Flask, jsonify
from app.extensions import db
from app.cli import register_cli



def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

     # Importer les  modèles ORM
    from app.auth.models import User
    from app.products.models import Product

    # Créer les tables
    with app.app_context():
        db.create_all()

    # Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.products.routes import products_bp
    app.register_blueprint(products_bp, url_prefix="/api/produits")

    # Créer user admin si nécessaire
    register_cli(app)

    # Par sécurité
    '''
    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        return jsonify({"message": "Internal server error"}), 500
    '''
    return app

    '''
@app.route('/predict', methods=["GET"])
@require_authentication
def predict():
    return {"message": "Ok !"}, 200
    '''