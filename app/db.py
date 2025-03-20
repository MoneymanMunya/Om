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
