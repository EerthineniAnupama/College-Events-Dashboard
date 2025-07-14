import mysql.connector
from mysql.connector import pooling

# Optional: Use connection pooling for efficiency
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "anupama@50lpa",
    "database": "events_db"
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
