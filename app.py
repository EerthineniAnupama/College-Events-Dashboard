from flask import Flask, render_template
from flask_cors import CORS
from routes.auth import auth_routes
from routes.events import event_routes
import os

# Ensure templates are picked from the correct folder
TEMPLATE_DIR = os.path.join(os.getcwd(), "templates")

app = Flask(__name__, static_folder='static',template_folder=TEMPLATE_DIR)
CORS(app)

# Register your API routes
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(event_routes, url_prefix="/api/events")

# -------------------------------
# Frontend Route Pages
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/organizer-dashboard")
def organizer_dashboard():
    return render_template("organizer-dashboard.html")

@app.route("/student-dashboard")
def student_dashboard():
    return render_template("student-dashboard.html")

@app.route("/create-event")
def create_event():
    return render_template("create-event.html")

@app.route("/edit-event")
def edit_event():
    return render_template("edit-event.html")

@app.route("/view-event/<int:event_id>")
def view_event(event_id):
    return render_template("view-event.html", event_id=event_id)


@app.route("/browse-events")
def browse_events():
    return render_template("browse-events.html")



# -------------------------------
# Run Flask App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
