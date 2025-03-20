import psycopg2

# Database connection settings
DB_NAME = "omni_db"
DB_USER = "postgres"
DB_PASSWORD = "Munya10"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    print("Users:", users)

    cursor.execute("SELECT * FROM tasks;")
    tasks = cursor.fetchall()
    print("Tasks:", tasks)

    cursor.close()
    conn.close()
    print("✅ Database connection successful")
except Exception as e:
    print("❌ Error connecting to database:", e)
import psycopg2
from psycopg2.extras import RealDictCursor

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="omni",
            user="postgres",
            password="Munya10",  # Your password
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        print("✅ Database connection successful!")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

# Test connection
if __name__ == "__main__":
    connect_db()
