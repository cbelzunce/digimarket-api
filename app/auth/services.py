from werkzeug.security import check_password_hash
from app.auth.repository import get_user_by_email

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)

    if not user:
        return None

    if not check_password_hash(user.password_hash, password):
        return None

    return user
