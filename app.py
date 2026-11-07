from flask import Flask, jsonify
from api.models import db
from api.routes import api_bp

def create_app():
    # initialize the Flask application
    app = Flask(__name__)

    # Configure SQLite database file stored locally
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with the app
    db.init_app(app)

    # Create database tables automatically if they don't exist
    with app.app_context():
        db.create_all()

    # Define a basic route for the root URL
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Welcome to your Flack backend",
            "status": "success"
        })

    # Register the blueprint with a URL prefix (e.g /api/greet becomes /api/v1/greet)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app

# Run the application in debug mode for development
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)