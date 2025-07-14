# 🎓 College Events Dashboard

An interactive full-stack web application for managing and participating in college events. Built with **Flask** (Python), **HTML/CSS/JS**, and **MySQL**, this dashboard provides dedicated interfaces for both students and organizers.

---

## 🚀 Features

### 👨‍🎓 For Students:
- 🔍 **Browse Events**: Filter and search upcoming events by date, title, or venue.
- 📝 **Register & Unregister**: Join or leave events with one click.
- 💬 **Comment System**: Post and view feedback for events.
- 📅 **Calendar Integration**: View registered events in calendar format.
- 📥 **Add to Calendar**: Download `.ics` calendar files for any event.
- 🖼️ **View Event Details**: See image, organizer contact, and full description in a modern popup view.

### 👩‍💼 For Organizers:
- 🛠️ **Create/Edit/Delete Events**: Manage event listings and images.
- 📄 **View Registrations**: See list of students registered per event.
- 🖼️ **Upload Event Images**: Each event has a visual preview.

---

## 🧠 Why This Project?

This project showcases:
- 🔐 **Role-based authentication & redirection**
- ⚡ **Frontend ↔ Backend Integration using REST API**
- 🗃️ **CRUD operations & image upload with secure storage**
- 💡 **Dynamic UI using Tailwind CSS and FullCalendar.js**
- 🎯 **MySQL relationships, foreign keys & queries**

---

## 🛠️ Tech Stack

| Technology        | Description                    |
|------------------|--------------------------------|
| Python + Flask   | Backend server and APIs        |
| HTML/CSS + JS    | Frontend UI (Vanilla JS + Tailwind) |
| MySQL            | Relational database            |
| FullCalendar.js  | Calendar view for events       |
| Jinja2           | Flask templating engine        |

---

## 📁 Folder Structure




---

## 🎥 Project Screenshots

### 🏠 Home Page
![Home](home.png)

### 🔐 Login Page
![Login](login.png)

### 📝 Create Account
![Create Account](create-account.png)

### 🎯 Browse Events
![Browse Events](browse-events.png)

### 🧑‍💼 Organizer Dashboard
![Organizer Dashboard](Organizer-dashboard.png)

### 🎓 Student Dashboard
![Student Dashboard](student-dashboard.png)

### 🔍 View Event
![View Event](view-event.png)

---

## 📖 How to Run Locally

### 🔄 Clone the repository

```bash
git clone https://github.com/EerthineniAnupama/College-Events-Dashboard.git
cd College-Events-Dashboard

🧪 Create & activate a virtual environment (optional but recommended)

python -m venv venv
venv\Scripts\activate    # Windows
# or
source venv/bin/activate  # Linux/Mac


📦 Install dependencies


pip install -r requirements.txt

Start the Flask server

python app.py

Open http://127.0.0.1:5000 in your browser and explore!

🌟 Final Note

This project is built from scratch to demonstrate full-stack development, API design, and real-world problem-solving. Perfect for showcasing backend logic, UI integration, database operations, and role-based functionalities.

If you find this helpful or impressive, feel free to ⭐ star the repo!


