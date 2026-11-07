from flask import Flask, jsonify, request
from api.routes import api_bp

def create_app():
    # initialize the Flask application
    app = Flask(__name__)

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