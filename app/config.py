import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///digimarket.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET = os.environ.get("JWT_SECRET", "dev-only-change-me")
    JWT_EXPIRES_MINUTES = int(os.environ.get("JWT_EXPIRES_MINUTES", "60"))
