from services.project_users_service import ProjectUsersService
from database.helpers import validate_jwt, generate_jwt

# Initialize service
project_users_service = ProjectUsersService()


class AuthService:
    @staticmethod
    def login(username: str, password: str):
        """ login and return auth token if successful """
        if not project_users_service.validate_user(username, password):
            return {"error": "Invalid username or password"}, 401
        
        user = project_users_service.get_user_by_username(username)
        token = generate_jwt(user["id"])
        
        if not token:
            return {"error": "Failed to generate auth token"}, 500
        
        return {"message": "Login successful", "token": token}, 200
        
    
    @staticmethod
    def validate_token(token: str):
        """ Check if the provided token is valid """
        if validate_jwt(token):
            return {"message": "Token is valid"}, 200
        else:
            return {"error": "Invalid or expired token"}, 401
        