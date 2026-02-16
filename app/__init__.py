from flask import Flask, request, jsonify
from app.auth.decorators import require_authentication
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def index():
    return "Coucou"

@app.route('/auth', methods=["POST"])
def auth():
    from .auth.security import generate_token

    body = request.get_json()
    if body and body.get("password", "") == "blent":
        token = generate_token("titi")

        return jsonify({"token": token}), 200
    return jsonify({"error": "Mot de passe invalide."}), 401

@app.route('/predict', methods=["GET"])
@require_authentication
def predict():
    return {"message": "Ok !"}, 200