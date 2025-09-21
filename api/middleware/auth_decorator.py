from functools import wraps
from flask import request, jsonify
from database.helpers import validate_auth_token

def token_required(f):
    """
    Decorator to require a valid auth token for accessing a route.
    Expects the token to be in the Authorization header as: Bearer <token>
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "error": "Authorization header is required",
                "message": "Please provide an Authorization header with a Bearer token"
            }), 401
        
        # Check if the header starts with "Bearer "
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "Invalid authorization format",
                "message": "Authorization header must be in format: Bearer <token>"
            }), 401
        
        # Extract the token
        token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                "error": "Token is required",
                "message": "Please provide a token after 'Bearer' in the Authorization header"
            }), 401
        
        # Validate the token
        if not validate_auth_token(token):
            return jsonify({
                "error": "Invalid or expired token",
                "message": "Please provide a valid authentication token"
            }), 401
        
        # If token is valid, proceed with the original function
        return f(*args, **kwargs)
    
    return decorated
