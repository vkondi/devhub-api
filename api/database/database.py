import os
import psycopg2
from psycopg2 import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def initialize_db():
    conn = get_connection()
    
    if not conn:
        print(f"Failed to connect to the database.")
        return
    
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS project_users (
                id SERIAL PRIMARY KEY,
                project_name VARCHAR(100) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)
        
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()