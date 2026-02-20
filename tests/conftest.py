import pytest
from app import create_app
from app.extensions import db

@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "JWT_SECRET": "test-secret",
        "JWT_EXPIRES_MINUTES": 60,
    })

    # Préparer une DB propre pour chaque test
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    # Nettoyage après le test
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()