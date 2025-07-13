from flask import Blueprint, request, jsonify
from db import get_db_connection
import bcrypt
import mysql.connector

auth_routes = Blueprint('auth', __name__)

# ------------------- Register Route -------------------
@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([name, email, password, role]):
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_password.decode('utf-8'), role)
        )
        conn.commit()
        return jsonify({"message": "Registration successful"}), 200

    except mysql.connector.errors.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Email already exists"}), 400
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Something went wrong"}), 500

    finally:
        cursor.close()
        conn.close()

# ------------------- Login Route -------------------
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({
                "name": user['name'],
                "email": user['email'],
                "role": user['role']
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Login failed"}), 500

    finally:
        cursor.close()
        conn.close()
