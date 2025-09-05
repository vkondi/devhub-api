from database import get_connection
import uuid
import datetime
import hashlib

"""
-------------------
Utility functions
-------------------
"""

def hash_password(password: str) -> str:
    # Generate SHA-256 hash of the password
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def generate_token() -> str:
    # Generate a unique token using UUID4
    return str(uuid.uuid4())

"""
-------------------
User management functions
-------------------
"""


"""
-------------------
Token management functions
-------------------
"""

