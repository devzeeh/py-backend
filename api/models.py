from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db

    def to_dict(self):
        """Helper method to convert database object to a dictionary for JSON responses"""
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email
        }