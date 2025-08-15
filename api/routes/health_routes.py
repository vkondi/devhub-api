from flask import Blueprint, jsonify

# Create a Blueprint for health check routes
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return jsonify({
        "status": "healthy",
        "message": "Devhub AI API is running"
    }), 200  