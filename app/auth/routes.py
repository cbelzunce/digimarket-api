from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request

from app.auth.models import User
from app.auth.security import generate_token
from app.auth.services import authenticate_user
from app.auth.validators import validate_connexion, validate_register
from app.extensions import db
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
        
    # Validation des champs
    errors = validate_register(data)
    if errors:
        return jsonify({"errors": errors}), 400
    print(1)
    email = data["email"].strip().lower()
    print(2)

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
    print(5)
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
    email = data.get("email")
    password = data.get("password")

    # Validation des champs
    errors = validate_connexion(data)

    if errors:
        return jsonify({"errors": errors}), 400  

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"message": "Identifiants invalides"}), 401  
    
    token = generate_token(
         user_id=user.id,
         email=user.email,
         roles=user.role
    )

    return jsonify({"access_token": token, "token_type": "Bearer"}), 200
