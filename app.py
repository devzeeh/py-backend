import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from api.models import db
from api.routes import api_bp

# Load enviroment variables from .env files
load_dotenv()

def create_app():
    # initialize the Flask application
    app = Flask(__name__)

    # Configure SQLite database file stored locally
    # configurations securely from environment variables with safe fallbacks
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback-secret-key")

    # Initialize extensions with the app
    db.init_app(app)
    jwt = JWTManager(app) # Initialize JWT manager
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Create database tables automatically if they don't exist
    with app.app_context():
        db.create_all()

    # Define a basic route for the root URL
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Welcome to your Flask backend",
            "status": "success"
        })

    # Register the blueprint with a URL prefix (e.g /api/greet becomes /api/v1/greet)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app

# Run the application in debug mode for development
if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app = create_app()
    app.run(debug=True, port=port)