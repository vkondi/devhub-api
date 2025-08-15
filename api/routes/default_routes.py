from flask import Blueprint, jsonify

# Create blueprint for default routes
default_bp = Blueprint('default', __name__)

@default_bp.route('/', methods=['GET'])
def index():
    """
    Default route that returns a welcome message.
    """
    return jsonify({"message": "Welcome to the DevHub API!"}), 200

@default_bp.route('/health')
def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return jsonify({
        "status": "healthy",
        "message": "Devhub AI API is running"
    }), 200  