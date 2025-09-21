from .database import get_connection
import uuid
import datetime
import jwt
import os
from argon2 import PasswordHasher
from psycopg2.extras import RealDictCursor

"""
-------------------
Utility functions
-------------------
"""

def hash_password(password: str) -> str:
    # Generate Argon2 hash of the password
    ph = PasswordHasher()
    return ph.hash(password)


def verify_hashed_password(stored_hash: str, password: str) -> bool:
    # Verify the provided password against the stored Argon2 hash
    ph = PasswordHasher()
    try:
        ph.verify(stored_hash, password)
        return True
    except:
        return False

def generate_token() -> str:
    # Generate a unique token using UUID4
    return str(uuid.uuid4())


"""
-------------------
Token management functions
-------------------
"""

def generate_jwt(user_id: int):
    """ Generate a JWT token for a given user_id """
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        print("JWT_SECRET_KEY not set in environment variables.")
        return None
    
    payload = {
        'user_id': user_id,
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)  # Token valid for 24 hours
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def validate_jwt(token: str):
    """ Validate a JWT token and return the payload if valid """
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        print("JWT_SECRET_KEY not set in environment variables.")
        return None
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None

  

