import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config_by_name
from extensions import db, jwt, migrate, limiter
from api.routes import api_bp
from api.errors import register_error_handlers

# Load enviroment variables from .env files
load_dotenv()

def create_app(config_name=None):
    # initialize the Flask application
    app = Flask(__name__)

    # Determine which config to use (default to 'development')
    if not config_name:
        config_name = os.getenv("FlASK_ENV")
    
    # Load the corresponding configuration class
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions with the app
    db.init_app(app)
    jwt = JWTManager(app) # Initialize JWT manager
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    # Connect limiter to the Flask app instance
    limiter.init_app(app)

    register_error_handlers(app)

    # Create database tables automatically if they don't exist
    with app.app_context():
        db.create_all()

    # Global ERROR HANDLER

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": str(error.description) if hasattr(error, 'description') else "Invalid request data",
            "status": 400
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource or endpoint does not exist",
            "status": 404
        }), 404 

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": "Unauthorized",
            "message": "Authentication token is missing or invalid",
            "status": 401
        }), 401

    @app.errorhandler(500)
    def internal_server_error(error):
        # In production, you'd log this error to a file or monitoring service
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server",
            "status": 500
        }), 500

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