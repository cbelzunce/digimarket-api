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


def require_role(required_role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if not hasattr(g, "user"):
                return jsonify({"message": "Authentification requise."}), 401

            user_payload = g.user

            # Cas 1 : token contient une liste "roles"
            roles = user_payload.get("roles")

            # Cas 2 : token contient un seul "role"
            if roles is None:
                role = user_payload.get("role")
                roles = [role] if role else []

            if required_role not in roles:
                return jsonify({"message": "Accès interdit."}), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator
