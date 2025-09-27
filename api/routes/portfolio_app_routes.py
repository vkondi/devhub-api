from flask import Blueprint, jsonify
from services.devto_service import DevToService
from middleware.auth_decorator import token_required
from extensions import cache

# Create a bluprint
portfolio_bp = Blueprint('portfolio', __name__)

# Initialize service(s)
devto_service = DevToService()

@portfolio_bp.route('/blogs', methods=['GET'])
@token_required
@cache.cached(timeout=10800)  # Cache this route for 3 hours
def get_blogs():
    """
    Endpoint to retrieve a list of blogs.
    Requires valid authentication token.
    """
    blogs = devto_service.get_articles()
    if blogs is None:
        return jsonify({"error": "Failed to fetch blogs"}), 500
    
    return jsonify({
        "message": "List of blogs",
        "blogs": blogs
    }), 200
