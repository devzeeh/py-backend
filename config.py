# config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    access_token_seconds = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 900))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=access_token_seconds)

    # Default rate-limiter storage (memory for local/tests, can be overridden by Redis in production)
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    RATELIMIT_ENABLED = True
    # Explicitly use memory storage for fast, isolated unit tests
    RATELIMIT_STORAGE_URI = "memory://"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    # In production, point this to a shared Redis cluster!
    # Example: RATELIMIT_STORAGE_URI = "redis://:password@localhost:6379"
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}