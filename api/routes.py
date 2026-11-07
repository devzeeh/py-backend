# api/routes.py
from flask import Blueprint, jsonify, request
from api.models import db, User

# Create a Blueprint named 'api
api_bp = Blueprint("api", __name__)

@api_bp.route("/users", methods=["GET"])
def get_user():
    """Fetch all user from the database"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200 

@api_bp.route("/users", methods=["POST"])
def create_user():
        """Save a new user to the database"""
        data = request.get_json()

        if not data or "name" not in data or "email" not in data:
            return jsonify({"error":"Missing 'name' or 'email' in request body"}), 400

        # Check if user if already exist
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        # Create new User instances
        new_user = User(name=data["name"], email=data["email"])

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user": new_user.to_dict()
        }), 201


@api_bp.route("/greet", methods=["POST"])
def greet_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    name = data.get("name")
    return jsonify({
        "greeting": f"Hello {name}! Your modular Flask backend is working."
    }), 200