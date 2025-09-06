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
    
@project_users_bp.route('/create', methods=['POST'])
def create_user():
    """
    Endpoint to create a new project user.
    Expects JSON body with 'project', 'username', and 'password' fields.
    """
    data = request.get_json()
    required_fields = ['project', 'username', 'password']
    
    print(f"Received data for new user: {data}")
    
    # Mandatory field check
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing one of the required fields: {required_fields}"}), 400
    
    project_name = data['project']
    username = data['username']
    password = data['password']
    
    # Empty field check
    if not project_name or not username or not password:
        return jsonify({"error": "Project name, username, and password cannot be empty"}), 400
    
    # Decrypt the password using RSA
    decrypted_password = rsa_manager.decrypt(password)
    if decrypted_password is None:
        return jsonify({"error": "Failed to decrypt password"}), 400
    
    # Hash the password before storing
    password_hash = hash_password(decrypted_password)
    
    new_user = project_users_service.create_user(project_name, username, password_hash)
    if new_user is None:
        return jsonify({"error": "Failed to create user"}), 500
    
    return jsonify({
        "message": "User created successfully",
        "user": new_user
    }), 201


@project_users_bp.route('/<string:username>', methods=['DELETE'])
def delete_user(username):
    """
    Endpoint to delete a project user by their username.
    """
    success = project_users_service.delete_user(username)
    if not success:
        return jsonify({"error": "Failed to delete user or user not found"}), 500
    
    return jsonify({
        "message": f"User {username} deleted successfully"
    }), 200
    
@project_users_bp.route('/activate', methods=['POST'])
def activate_user():
    """
    Endpoint to activate a project user.
    Expects JSON body with 'username' field.
    """
    data = request.get_json()
    
    # Mandatory field check
    if not data or 'username' not in data:
        return jsonify({"error": "Missing 'username' in request body"}), 400
    
    username = data['username']
    
    # Empty field check
    if not username:
        return jsonify({"error": "Username cannot be empty"}), 400
    
    success = project_users_service.activate_user(username)
    if not success:
        return jsonify({"error": "Failed to activate user or user not found"}), 500
    
    return jsonify({
        "message": f"User {username} activated successfully"
    }), 200
    

@project_users_bp.route('/deactivate', methods=['POST'])
def deactivate_user():
    """
    Endpoint to deactivate a project user.
    Expects JSON body with 'username' field.
    """
    data = request.get_json()
    
    # Mandatory field check
    if not data or 'username' not in data:
        return jsonify({"error": "Missing 'username' in request body"}), 400
    
    username = data['username']
    
    # Empty field check
    if not username:
        return jsonify({"error": "Username cannot be empty"}), 400
    
    success = project_users_service.deactivate_user(username)
    if not success:
        return jsonify({"error": "Failed to deactivate user or user not found"}), 500
    
    return jsonify({
        "message": f"User {username} deactivated successfully"
    }), 200