from flask import jsonify
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

def register_error_handlers(app):
    """Register custom JSON error handlers globally on the Flask app"""

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "error": "Bad Request",
            "message": str(e.description) if hasattr(e, "description") else "Invalid request syntax"
        }), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource or endpoint does not exist"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "error": "Method Not Allowed",
            "message": "The HTTP method is not supported for this endpoint"
        }), 405

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e):
        """Catches database constraint violations (e.g., unique email conflicts)"""
        # Roll back the failed transaction to keep the session clean
        from extensions import db
        db.session.rollback()
        
        return jsonify({
            "error": "Conflict Error",
            "message": "A database constraint was violated (e.g., email already exists)."
        }), 409

    @app.errorhandler(500)
    def internal_server_error(e):
        """Catch-all safety net for unexpected server crashes"""
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server. Please try again later."
        }), 500