import pytest
from app import create_app
from api.models import db as _db

@pytest.fixture
def app():
    """Create and configure a fresh Flask app instance fro testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        # Use an in-memory SQLite database for fast, isolated tests
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    """A test client that can send mock HTTP request to API"""
    return app.test_client()