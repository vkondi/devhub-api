from database.database import get_connection
from psycopg2.extras import RealDictCursor
import datetime

class ProjectUsersService:
    """
    Service to manage project users
    """
    
    def __init__(self):
        pass
    
    def get_all_users(self):
        """
        Retrieve all project users from the database.
        """
        conn = get_connection()
        if not conn:
            print("Failed to connect to the database.")
            return None
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("SELECT id, project_name, username, created_at, is_active FROM project_users;")
            users = cur.fetchall()
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return None
        finally:
            cur.close()
            conn.close()
            
    def get_user_by_username(self, username: str):
        """
        Retrieve a project user by their Username.
        """
        conn = get_connection()
        if not conn:
            print("Failed to connect to the database.")
            return None
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("SELECT id, project_name, username, password_hash, created_at, is_active FROM project_users WHERE username = %s;", (username,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching user by ID: {e}")
            return None
        finally:
            cur.close()
            conn.close()
            
    def create_user(self, project_name: str, username: str, password_hash: str):
        """
        Create a new project user.
        """
        conn = get_connection()
        if not conn:
            print("Failed to connect to the database.")
            return None
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("""
                INSERT INTO project_users (project_name, username, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, project_name, username, created_at, is_active;
            """, (project_name, username, password_hash))
            
            new_user = cur.fetchone()
            conn.commit()
            return new_user
        except Exception as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return None
        finally:
            cur.close()
            conn.close()
                
    def delete_user(self, username: str) -> bool:
        """
        Delete a project user by their username.
        """
        conn = get_connection()
        if not conn:
            print("Failed to connect to the database.")
            return False
        
        cur = conn.cursor()
        
        try:
            cur.execute("DELETE FROM project_users WHERE username = %s;", (username,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
            
    def activate_user(self, username: str) -> bool:
        """
        Activate a project user account.
        """
        conn = get_connection()
        if not conn:
            print("Failed to connect to the database.")
            return False
        
        cur = conn.cursor()
        
        try:
            cur.execute("UPDATE project_users SET is_active = TRUE WHERE username = %s;", (username,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Error activating user: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
            
    def deactivate_user(self, username: str) -> bool:
        """
        Deactivate a project user account.
        """
        conn = get_connection()
        if not conn:
            print("Failed to connect to the database.")
            return False
        
        cur = conn.cursor()
        
        try:
            cur.execute("UPDATE project_users SET is_active = FALSE WHERE username = %s;", (username,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Error deactivating user: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()