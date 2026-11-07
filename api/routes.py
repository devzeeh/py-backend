# api/routes.py
from flask import Blueprint, jsonify, request

# Create a Blueprint named 'api
api_bp = Blueprint("api", __name__)

@api_bp.route("/greet", methods=["POST"])
def greet_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    name = data.get("name")
    return jsonify({
        "greeting": f"Hello {name}! Your modular Flask backend is working."
    }), 200