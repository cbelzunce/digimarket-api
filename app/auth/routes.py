from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request

from app.auth.models import User
from app.auth.security import generate_token
from app.auth.users_store import get_user_by_username, verify_password
from app.extensions import db
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    
    '''
    # Validation des champs
    errors = validate_register(data)
    if errors:
        return jsonify({"errors": errors}), 400
    '''

    email = data["email"].strip().lower()
    
     # Création de l'utilisateur
    user = User(
        email=email,
        password_hash=generate_password_hash(data["password"]),
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        role="client"
    )

    # Ajout en base
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "L'email existe déjà"}), 409
    
    # et return ses infos sauf pass
    return jsonify({
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role
    }), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password: # Sortir les checks 
        return jsonify({"message": "Nom et mot de passe requis"}), 400

    user = get_user_by_username(username)

    if not user or not verify_password(user, password):
            return jsonify({"message": "Identifiants invalides"}), 401
    
    token = generate_token(
         user_id=user["id"],
         username=user["username"],
         roles=user["roles"]
    )

    return jsonify({"access_token": token, "token_type": "Bearer"}), 200
