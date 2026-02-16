from flask import Flask, request, jsonify
from app.auth.decorators import require_authentication
from app.auth.security import generate_token
from app.auth.users_store import get_user_by_username, verify_password

app = Flask(__name__)


@app.route('/auth/login', methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
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


@app.route('/predict', methods=["GET"])
@require_authentication
def predict():
    return {"message": "Ok !"}, 200