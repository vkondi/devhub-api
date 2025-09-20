from services.project_users_service import ProjectUsersService
from database.helpers import create_auth_token, validate_auth_token, revoke_auth_token

# Initialize service
project_users_service = ProjectUsersService()


class AuthService:
    @staticmethod
    def login(username: str, password: str):
        """ login and return auth token if successful """
        if not project_users_service.validate_user(username, password):
            return {"error": "Invalid username or password"}, 401
        
        user = project_users_service.get_user_by_username(username)
        token = create_auth_token(user["id"])
        
        if not token:
            return {"error": "Failed to generate auth token"}, 500
        
        return {"message": "Login successful", "token": token["token"], "expires_at": token["expires_at"]}, 200
        
    
    @staticmethod
    def validate_token(token: str):
        """ Check if the provided token is valid """
        if validate_auth_token(token):
            return {"message": "Token is valid"}, 200
        else:
            return {"error": "Invalid or expired token"}, 401
        
    @staticmethod
    def logout(token: str):
        """ Revoke the provided auth token """
        if revoke_auth_token(token):
            return {"message": "Logged out successfully"}, 200
        else:
            return {"error": "Failed to logout"}, 400