from functools import wraps
from flask import request

def require_authentication(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        from ..auth.security import decode_token

        token = request.headers.get("Authorization", "")

        if not token or not decode_token(token):
            return {"error": "Jeton d'accès invalide."}, 401
        
        return f(*args, **kwargs)
    return wrapper