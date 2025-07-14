import os
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()  # Load from .env

dbconfig = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME"),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="events_pool",
    pool_size=5,
    **dbconfig
)

def get_db_connection():
    try:
        conn = connection_pool.get_connection()
        return conn
    except Exception as err:
        print("❌ DB connection failed:", err)
        return None
