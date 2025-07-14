import os
from mysql.connector import pooling

dbconfig = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME")
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="events_pool",
    pool_size=5,
    **dbconfig
)

def get_db_connection():
    try:
        return connection_pool.get_connection()
    except Exception as e:
        print("❌ MySQL connection error:", e)
        return None
