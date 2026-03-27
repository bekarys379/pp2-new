import psycopg2
from config import DB_config

def get_connection():
    try:
        with psycopg2.connect(**DB_config) as conn:
            print("Connected to PostgreSQL server.")

    except Exception as e:
        print(f"Database error:{e}")





