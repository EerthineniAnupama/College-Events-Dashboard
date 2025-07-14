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

    # Validation
    if not all([name, email, password, role]):
        return jsonify({"error": "All fields are required"}), 400

    # Hash password
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
        return jsonify({"error": "Database integrity error"}), 500

    except Exception as e:
        print("❌ Exception during registration:", e)
        return jsonify({"error": "Internal server error"}), 500

    finally:
        cursor.close()
        conn.close()

# ------------------- Login Route -------------------
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validation
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
        print("❌ Exception during login:", e)
        return jsonify({"error": "Login failed"}), 500

    finally:
        cursor.close()
        conn.close()
