import jwt
from flask import current_app
from datetime import datetime, timedelta, timezone

JWT_ALGORITHM = "HS256"

def generate_token(user_id: int, email: str, roles: list[str]):
    now = datetime.now(timezone.utc)

    secret = current_app.config["JWT_SECRET"]
    expires_minutes = int(current_app.config.get("JWT_EXPIRES_MINUTES", 60))

    payload = {
        "sub": str(user_id),
        "user": email,
        "roles": roles,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }

    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    secret = current_app.config["JWT_SECRET"]

    return jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
