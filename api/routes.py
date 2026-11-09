# api/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, User, Task

# Create a Blueprint named 'api
api_bp = Blueprint("api", __name__)

@api_bp.post("/register")
def register():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing name, email, password"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(name=data["name"], email=data["email"])
    new_user.set_password(data["password"]) # securely hash password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully", 
        "user": new_user.to_dict()
        }), 201

@api_bp.post("/login")
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

@api_bp.get("/profile")
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

@api_bp.get("/tasks")
@jwt_required()
def get_user_tasks():
    """Fetch only the tasks belonging to the currently logged in"""
    current_user_id = get_jwt_identity()

    # Read query parameters from the URL (With safe defaults)
    # /api/v1/tasks?page=1&per_page=5
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Optional filter: check if user wants only completed or active tasks
    # Example URL: /api/v1/tasks?done=true
    done_param = request.args.get("done")

    # Build base query
    query = Task.query.filter_by(user_id=current_user_id)

    if done_param is not None:
        # Convert string 'true'/'false' to boolean
        is_done = done_param.lower() == 'true'
        query = query.filter_by(done=is_done)

    # Apply pagination using SQLAlchemy .paginate()
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    tasks = pagination.items    

    # Return paginated response with helpful metadata for the frontend
    return jsonify({
        "tasks": [task.to_dict() for task in tasks],
        "pagination": {
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }), 200

@api_bp.post("/tasks")
@jwt_required()
def create_task():
    """Create a new task tied securely to the logged-in user"""
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Missing task title"}), 400

    new_task = Task(
        title=data["title"],
        user_id=current_user_id # bind task to token holder
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully",
        "task": new_task.to_dict()
    }), 201

@api_bp.put("/tasks/<int:task_id>")
@jwt_required()
def update_task(task_id):
    """Update a specific task (toggle 'done' status or change title)"""
    current_user_id = get_jwt_identity()

    # Fetch the task or return a 404 error if it doesn't exist
    task = Task.query.get_or_404(task_id)

    # SECURITY CHECK: Ensure the logged-in user owns this task
    # Note: convert to string just in case JWT identity is stored as a string
    if str(task.user_id) != str(current_user_id):
        return jsonify({"error": "Unauthorized: You do not own this task"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    # Update fields if provided in the request
    if "title" in data:
        task.title = data["title"]
    if "done" in data:
        task.done = data["done"]

    db.session.commit()

    return jsonify({
        "message": "Task updated successfully",
        "task": task.to_dict()
    }), 200

@api_bp.delete("/tasks/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    """Delete a specific task belonging to the logged-in user"""
    current_user_id = get_jwt_identity()
    
    # If the task doesn't exist, SQLAlchemy automatically raises a 404 
    # and our global error handler returns a clean JSON response!
    task = Task.query.get_or_404(task_id)
    
    if str(task.user_id) != str(current_user_id):
        return jsonify({"error": "Unauthorized: You do not own this task"}), 403

    db.session.delete(task)
    db.session.commit() 

    return jsonify({"message": "Task deleted successfully"}), 200

@api_bp.get("/users")
def get_user():
    """Fetch all user from the database"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200 

@api_bp.post("/users")
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


@api_bp.post("/greet")
def greet_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    name = data.get("name")
    return jsonify({
        "greeting": f"Hello {name}! Your modular Flask backend is working."
    }), 200