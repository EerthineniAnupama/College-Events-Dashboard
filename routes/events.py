from flask import Blueprint, request, jsonify
from db import get_db_connection
from datetime import datetime, date
from werkzeug.utils import secure_filename
import os

event_routes = Blueprint('event_routes', __name__)

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------
# 1. Create Event
# -------------------------
@event_routes.route('/create', methods=['POST'])
def create_event():
    title = request.form.get('title')
    description = request.form.get('description')
    date_str = request.form.get('date')
    venue = request.form.get('venue')
    registration_link = request.form.get('registration_link')
    contact_email = request.form.get('contact_email')
    contact_phone = request.form.get('contact_phone')
    organizer = request.form.get('organizer')
    image = request.files.get('image')

    if not all([title, description, date_str, venue, organizer]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    if not image or image.filename == '':
        return jsonify({"error": "Image is required"}), 400

    filename = secure_filename(image.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)
    image_url = f"/static/uploads/{filename}".replace("\\", "/")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT role FROM users WHERE name = %s", (organizer,))
        user = cursor.fetchone()
        if not user or user[0] != "organizer":
            return jsonify({"error": "Only organizers can create events"}), 403

        cursor.execute("""
            INSERT INTO events (title, description, date, venue, registration_link,
                                contact_email, contact_phone, organizer, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, description, date_str, venue, registration_link,
              contact_email, contact_phone, organizer, image_url))
        conn.commit()
        return jsonify({"message": "Event created"}), 200

    except Exception as e:
        print("❌ Error creating event:", e)
        return jsonify({"error": "Server error"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 2. Get Events by Organizer
# -------------------------
@event_routes.route('/by-organizer', methods=['GET'])
def get_events_by_organizer():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Organizer name required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM events WHERE organizer = %s", (name,))
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        print("❌ Error fetching organizer events:", e)
        return jsonify({"error": "Error fetching events"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 3. Get Student Registered Events
# -------------------------
@event_routes.route('/student/<email>/events', methods=['GET'])
def get_registered_events(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.id, e.title, e.date, e.venue, e.description, e.image_url
            FROM registrations r
            JOIN events e ON r.event_id = e.id
            WHERE r.student_email = %s
        """, (email,))
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        print("❌ Fetching registered events failed:", e)
        return jsonify({"error": "Could not fetch events"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 4. Register for Event
# -------------------------
@event_routes.route('/register', methods=['POST'])
def register_event():
    data = request.get_json()
    event_id = data.get('event_id')
    student_email = data.get('student_email')

    if not event_id or not student_email:
        return jsonify({'error': 'Missing event_id or student_email'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (student_email,))
        if not cursor.fetchone():
            return jsonify({'error': 'Student not found'}), 400

        cursor.execute("SELECT * FROM registrations WHERE event_id = %s AND student_email = %s",
                       (event_id, student_email))
        if cursor.fetchone():
            return jsonify({'message': 'Already registered'}), 200

        cursor.execute("INSERT INTO registrations (event_id, student_email) VALUES (%s, %s)",
                       (event_id, student_email))
        conn.commit()
        return jsonify({'message': 'Registered successfully'}), 200

    except Exception as e:
        print("❌ Registration failed:", e)
        return jsonify({'error': 'Registration failed'}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 5. Get Event by ID
# -------------------------
@event_routes.route('/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(event), 200
    except Exception as e:
        print("❌ Fetch by ID failed:", e)
        return jsonify({"error": "Error fetching event"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 6. Post Comment
# -------------------------
@event_routes.route('/comment', methods=['POST'])
def post_comment():
    data = request.get_json()
    event_id = data.get('event_id')
    student_email = data.get('email')
    content = data.get('content')

    if not all([event_id, student_email, content]):
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO comments (event_id, student_email, content)
            VALUES (%s, %s, %s)
        """, (event_id, student_email, content))
        conn.commit()
        return jsonify({"message": "Comment posted"}), 200
    except Exception as e:
        print("❌ Comment post failed:", e)
        return jsonify({"error": "Failed to post comment"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 7. Get Comments
# -------------------------
@event_routes.route('/comments/<int:event_id>', methods=['GET'])
def get_comments(event_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT student_email, content, created_at
            FROM comments
            WHERE event_id = %s
            ORDER BY created_at DESC
        """, (event_id,))
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        print("❌ Fetch comments failed:", e)
        return jsonify({"error": "Failed to fetch comments"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 8. Upcoming Events
# -------------------------
@event_routes.route('/upcoming-events', methods=['GET'])
def get_upcoming_events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM events WHERE date >= %s ORDER BY date ASC", (date.today(),))
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        print("❌ Fetch upcoming events failed:", e)
        return jsonify({"error": "Failed to fetch upcoming events"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 9. Browse Events
# -------------------------
@event_routes.route('/browse', methods=['GET'])
def browse_events():
    return get_upcoming_events()

# -------------------------
# 10. Unregister Event
# -------------------------
@event_routes.route('/unregister', methods=['DELETE'])
def unregister_event():
    data = request.get_json()
    email = data.get('email')
    event_id = data.get('event_id')

    if not email or not event_id:
        return jsonify({"error": "Missing email or event_id"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM registrations WHERE student_email = %s AND event_id = %s", (email, event_id))
        conn.commit()
        return jsonify({"message": "Unregistered successfully"}), 200
    except Exception as e:
        print("❌ Unregister failed:", e)
        return jsonify({"error": "Unregistration failed"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 11. Delete Event
# -------------------------
@event_routes.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
        conn.commit()
        return jsonify({"message": "Event deleted successfully"}), 200
    except Exception as e:
        print("❌ Delete failed:", e)
        return jsonify({"error": "Could not delete event"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 12. Get Registrations for Event
# -------------------------
@event_routes.route('/<int:event_id>/registrations', methods=['GET'])
def get_event_registrations(event_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT student_email FROM registrations WHERE event_id = %s", (event_id,))
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        print("❌ Fetch registrations failed:", e)
        return jsonify({"error": "Could not fetch registrations"}), 500
    finally:
        cursor.close()
        conn.close()

# -------------------------
# 13. Update Event
# -------------------------
@event_routes.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    title = data.get('title')
    date_str = data.get('date')
    venue = data.get('venue')
    description = data.get('description')

    if not all([title, date_str, venue, description]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE events
            SET title = %s, date = %s, venue = %s, description = %s
            WHERE id = %s
        """, (title, date_str, venue, description, event_id))
        conn.commit()
        return jsonify({"message": "Event updated"}), 200
    except Exception as e:
        print("❌ Update failed:", e)
        return jsonify({"error": "Update failed"}), 500
    finally:
        cursor.close()
        conn.close()
