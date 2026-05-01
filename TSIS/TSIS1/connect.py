def get_connection():
    try:
        return psycopg2.connect(**DB_config)
    except Exception as e:
        print(f"Database error: {e}")
        return None
