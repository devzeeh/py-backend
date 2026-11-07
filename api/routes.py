# api/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, User

# Create a Blueprint named 'api
api_bp = Blueprint("api", __name__)

@api_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing name, email, password"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email alreadt registered"}), 400

    new_user = User(name=data["name"], email=data["email"])
    new_user.set_password(data["password"]) # securely hash password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully!", 
        "user": new_user.to_dict()
        }), 201

@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    # Check if user exists and password matches
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create a JWT token containing the user's ID as identity
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "access_token": access_token
    }), 200

@api_bp.route("/profile", methods=["GET"])
@jwt_required() # This decorator forces the client to send a valid token!
def get_profile():
    # Get the user ID stored inside the JWT token
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "Access granted to protected route!",
        "user": user.to_dict()
    }), 200


        
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