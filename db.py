import mysql.connector

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anupama@50lpa",
            database="events_db"
        )
        return conn
    except mysql.connector.Error as err:
        print("❌ MySQL connection failed:", err)
        return None
