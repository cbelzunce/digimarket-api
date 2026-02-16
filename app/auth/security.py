import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET = os.environ["JWT_SECRET"] 

def generate_token(user):
    return jwt.encode(
        {
            "exp": datetime.now() + timedelta(hours=1),
            "user": user
        },
        JWT_SECRET,
        algorithm="HS256"
    )

def decode_token(token):
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms="HS256"
        )
    except Exception:
        print("Jeton JWT invalide.")
        return
