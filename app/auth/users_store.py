from werkzeug.security import generate_password_hash, check_password_hash

_USERS = {
    "titi": {
        "id": 1,
        "username": "titi",
        "password_hash": generate_password_hash("blent"),
        "roles": ["user"],
    }
}

def get_user_by_username(username: str):
    return _USERS.get(username)


def verify_password(user, password: str) -> bool:
    return check_password_hash(user["password_hash"], password)