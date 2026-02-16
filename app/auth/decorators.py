from functools import wraps
from flask import request, jsonify, g
from .security import decode_token


def require_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")

        if not auth.startswith("Bearer "):
            return jsonify({"message": "Authorization header manquant ou invalide"}), 401

        token = auth.split(" ", 1)[1].strip()

        try:
            payload = decode_token(token)
        except Exception as e:
            return jsonify({"message": "Token invalide"}), 401

        # On stocke l'identité pour la suite du traitement
        g.user = payload        
        return func(*args, **kwargs)
    return wrapper