# config.py
import os
from datetime import timedelta

class Config:
    """Base configuration with default settings"""
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    access_token_seconds = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 900))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=access_token_seconds)

class DevelopmentConfig(Config):
    """Configuration for local development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")

class TestingConfig(Config):
    """Configuration for automated tests (Pytest)"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProductionConfig(Config):
    """Configuration for production deployment"""
    DEBUG = False
    # In production, require strict environment variables or fail fast
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

# A handy dictionary to pick the right config easily
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}