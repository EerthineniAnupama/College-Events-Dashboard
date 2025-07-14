# 🎓 College Events Dashboard

An interactive full-stack web application for managing and participating in college events. Built with **Flask** (Python), **HTML/CSS/JS**, and **MySQL**, this dashboard provides dedicated interfaces for both students and organizers.

---

## 🚀 Features

### 👨‍🎓 For Students:
- 🔍 **Browse Events**: Filter and search upcoming events by date, title, or venue.
- 📝 **Register & Unregister**: Join events directly from the dashboard.
- 💬 **Comment System**: Post and view feedback for any event.
- 📅 **Calendar Integration**: See all registered events in a calendar view.
- 📥 **Add to Google/Local Calendar**: Download `.ics` calendar files.
- 🖼️ **View Event Details**: Including image, organizer contact, and full description.

### 👩‍💼 For Organizers:
- 🛠️ **Create/Edit/Delete Events**: Manage event details and images.
- 📄 **View Registrations**: Access list of students registered for each event.
- 🖼️ **Upload Event Image**: Event images stored and displayed dynamically.

---

## 🧠 Why This Project?

This project demonstrates:
- 🔐 **Role-based authentication**
- ⚡ **Frontend-Backend Integration**
- 🗃️ **CRUD operations with file upload handling**
- 📊 **Dynamic UI with Tailwind CSS and FullCalendar.js**
- 🎯 **Practical use of REST APIs & MySQL foreign key relationships**

---

## 🛠️ Tech Stack

| Tech             | Role                          |
|------------------|-------------------------------|
| Python + Flask   | Backend Server & Routing      |
| HTML/CSS + JS    | Frontend (Vanilla JS + Tailwind CSS) |
| MySQL            | Database                      |
| FullCalendar.js  | Event calendar integration    |
| Jinja2           | Templating with Flask         |

---

## 📁 Folder Structure

events-dashboard-backend/
│
├── static/
│ └── uploads/ # Uploaded event images
├── templates/ # HTML frontend pages
│ ├── index.html
│ ├── login.html
│ ├── student-dashboard.html
│ ├── organizer-dashboard.html
│ └── ...
├── routes/
│ ├── init.py
│ ├── auth.py # Login/Register routes
│ └── events.py # All event-related APIs
├── db.py # DB connection logic
├── app.py # Main Flask app entry
└── README.md # You're reading it :)

Screenshots 

## 🎥 Project Screenshots

### 🏠 Home Page
![Home](home.png)




### 🔐 Login Page
![Login](./login.png)

### 📝 Create Account
![Create Account](create-account.png)

### 🎯 Browse Events
![Browse Events](./browse-events.png)

### 🧑‍💼 Organizer Dashboard
![Organizer Dashboard](./Organizer-dashboard.png)

### 🎓 Student Dashboard
![Student Dashboard](./student-dashboard.png)

### 🔍 View Event
![View Event](./view-event.png)

📖 How to Run Locally

Clone the repository

git clone https://github.com/EerthineniAnupama/College-Events-Dashboard.git
cd College-Events-Dashboard

Create and activate virtual environment (optional but recommended)

python -m venv venv
venv\Scripts\activate    # Windows
# or
source venv/bin/activate  # Linux/Mac

Install dependencies

pip install -r requirements.txt

Start the Flask server

python app.py

Open http://127.0.0.1:5000 in your browser and explore!

🌟 Final Note

This project is built from scratch to demonstrate full-stack development, API design, and real-world problem-solving. Perfect for showcasing backend logic, UI integration, database operations, and role-based functionalities.

If you find this helpful or impressive, feel free to ⭐ star the repo!


