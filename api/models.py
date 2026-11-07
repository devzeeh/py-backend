from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) # Store hash, not plain text!
    role = db.Column(db.String(20), default="user", nullable=False)

    # Establish relationship: One user has many tasks
    # cascade="all, delete-orphan" means if a user is deleted, their tasks are deleted too
    tasks = db.relationship('Task', backref='author', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """hash the password before saving"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the store hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Helper method to convert database object to a dictionary for JSON responses"""
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

    # Foreign Key linking this task to a specific User ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "user_id": self.user_id
        }