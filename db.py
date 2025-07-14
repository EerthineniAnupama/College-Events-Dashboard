import mysql.connector
from mysql.connector import pooling
import os

# Optional: Use connection pooling for efficiency
dbconfig = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "events_db"),
    "port": int(os.environ.get("DB_PORT", 3306))  # ✅ Fallback to default
}

# Create a connection pool with a max of 5 connections
connection_pool = pooling.MySQLConnectionPool(pool_name="events_pool",
                                              pool_size=5,
                                              **dbconfig)

def get_db_connection():
    try:
        conn = connection_pool.get_connection()
        return conn
    except mysql.connector.Error as err:
        print("❌ MySQL connection failed:", err)
        return None
