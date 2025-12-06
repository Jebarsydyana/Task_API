Task Management API
Project Overview

This project is a simple Task Management Application built as a part of the SuPrazo Technologies Jr. Software Developer Intern Assessment.
It includes a backend REST API using Flask and a basic frontend interface using HTML, CSS, and JavaScript.
The application allows users to:

Create a task
View tasks
Update task status
Delete tasks

Tools & Technologies Used

Backend -Python, Flask, Flask-CORS
Storage	- JSON file (tasks.json)
Frontend - HTML, CSS, JavaScript (Fetch API)
Testing	- curl
Editor - Visual Studio Code
OS - Ubuntu

How to Run the Project
Setup & Run Backend
Open terminal and run:

cd backend
source ../venv/bin/activate
pip install -r requirements.txt
python app.py

Backend will run at:

http://127.0.0.1:5000

Run Frontend
Open another terminal:

cd frontend
python3 -m http.server 8000

Open the app in browser:

http://127.0.0.1:8000/index.html
