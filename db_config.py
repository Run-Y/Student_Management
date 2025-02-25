import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "project",
    "user": "postgres",
    "password": "1263006339"
}

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Failed:", e)
        return None
