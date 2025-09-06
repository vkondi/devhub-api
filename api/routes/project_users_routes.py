from flask import Blueprint, jsonify, request
from services.project_users_service import ProjectUsersService
from services.rsa_encryption_service import RSAEncryption
from database.helpers import hash_password

# Create a blueprint
project_users_bp = Blueprint('project_users', __name__)

# Initialize service
project_users_service = ProjectUsersService()
rsa_manager = RSAEncryption()

@project_users_bp.route('/', methods=['GET'])
def get_all_users():
    """
    Endpoint to retrieve all project users.
    """
    users = project_users_service.get_all_users()
    if users is None:
        return jsonify({"error": "Failed to fetch users"}), 500
    
    return jsonify({
        "message": "List of project users",
        "users": users
    }), 200
    
@project_users_bp.route('/<string:username>', methods=['GET'])
def get_user_by_username(username):
    """
    Endpoint to retrieve a project user by their username.
    """
    user = project_users_service.get_user_by_username(username)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "message": f"Details of user {username}",
        "user": user
    }), 200
    
@project_users_bp.route('/', methods=['POST'])
def create_user():
    """
    Endpoint to create a new project user.
    Expects JSON body with 'project', 'username', and 'password' fields.
    """
    data = request.get_json()
    required_fields = ['project', 'username', 'password']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing one of the required fields: {required_fields}"}), 400
    
    
    decrypted_password = rsa_manager.decrypt(data['password'])
    if decrypted_password is None:
        return jsonify({"error": "Failed to decrypt password"}), 400
    
    
    project_name = data['project']
    username = data['username']
    password_hash = hash_password(decrypted_password)
    
    user_id = project_users_service.create_user(project_name, username, password_hash)
    if user_id is None:
        return jsonify({"error": "Failed to create user"}), 500
    
    return jsonify({
        "message": "User created successfully",
        "userId": user_id
    }), 201
