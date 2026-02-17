from app.extensions import db
from app.auth.models import User

def get_user_by_email(email: str) -> User | None:
    return db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()
