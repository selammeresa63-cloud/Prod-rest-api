import os
from datetime import timedelta

def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value

class Config:
    SECRET_KEY = _required_env("SECRET_KEY")
    JWT_SECRET_KEY = _required_env("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = _required_env("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ERROR_MESSAGE_KEY = "message"

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "testing-secret"
    JWT_SECRET_KEY = "testing-jwt-secret"

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
