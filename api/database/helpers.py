from .database import get_connection
import uuid
import datetime
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

def create_auth_token(project_id: int, expires_in_hours: int = 24):
    """ Create and store token for a given project_id """
    
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database.")
        return None
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        token = generate_token()
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=expires_in_hours)
        
        cur.execute("""
            INSERT INTO auth_tokens (project_id, token, expires_at)
            VALUES (%s, %s, %s)
            RETURNING id, project_id, token, expires_at, created_at;   
        """, (project_id, token, expires_at))
        
        new_token = cur.fetchone()
        conn.commit()
        return new_token
    except Exception as e:
        print(f"Error creating auth token: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def validate_auth_token(token: str) -> bool:
    """ Validate if a token is valid and not expired """
    
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database.")
        return False
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            SELECT * from auth_tokens
            WHERE token = %s and expires_at > NOW();
        """, (token,))
        result = cur.fetchone()
        return result is not None
        
    except Exception as e:
        print(f"Error validating auth token: {e}")
        return False
    finally:
        cur.close()
        conn.close()
        

def revoke_auth_token(token: str) -> bool:
    """ Revoke (delete) a token """
    
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database.")
        return False
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            DELETE from auth_tokens
            WHERE token = %s;
        """,(token,))
        deleted = cur.rowcount > 0
        conn.commit()
        return deleted
    except Exception as e:
        print(f"Error revoking auth token: {e}")
        return False
    finally:
        cur.close()
        conn.close()

     
def revoke_expired_tokens() -> bool:
    """ Revoke all expired tokens """
    
    conn = get_connection()
    if not conn:
        print("Failed to connect to the database.")
        return False
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            DELETE from auth_tokens
            WHERE expires_at <= NOW();
        """)
        deleted_count = cur.rowcount > 0
        conn.commit()
        return deleted_count
    except Exception as e:
        print(f"Error revoking expired tokens: {e}")
        return False
    finally:
        cur.close()
        conn.close()