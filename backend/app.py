from flask import Flask, jsonify, request
import json
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Path to JSON "database" file
DATA_FILE = "tasks.json"


def load_tasks():
    """
    Load tasks from the JSON file.
    Returns a list of task dictionaries.
    """
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            # Ensure it's always a list
            if isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            # If file is empty or corrupted, return empty list
            return []


def save_tasks(tasks):
    """
    Save the list of tasks to the JSON file.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks):
    """
    Generate the next ID based on existing tasks.
    """
    if not tasks:
        return 1
    # Max existing id + 1
    return max(task["id"] for task in tasks) + 1


@app.route("/", methods=["GET"])
def index():
    """
    Simple welcome route.
    """
    return jsonify({
        "message": "Welcome to the Task Management API",
        "endpoints": {
            "GET /tasks": "Get all tasks",
            "GET /tasks/<id>": "Get a task by ID",
            "POST /tasks": "Create a new task",
            "PUT /tasks/<id>": "Update an existing task",
            "DELETE /tasks/<id>": "Delete a task"
        }
    }), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """
    Get all tasks.
    """
    tasks = load_tasks()
    return jsonify(tasks), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """
    Get a single task by ID.
    """
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    """
    Create a new task.
    Expected JSON body: { "title": "...", "description": "...", "completed": false }
    'title' is mandatory. 'completed' defaults to False.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title")
    description = data.get("description", "")
    completed = data.get("completed", False)

    if not title or not isinstance(title, str):
        return jsonify({"error": "Field 'title' is required and must be a string"}), 400

    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "title": title.strip(),
        "description": description.strip() if isinstance(description, str) else "",
        "completed": bool(completed)
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify({
        "message": "Task created successfully",
        "task": new_task
    }), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """
    Update an existing task.
    Expected JSON body (any of these fields): { "title": "...", "description": "...", "completed": true/false }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    title = data.get("title", task["title"])
    description = data.get("description", task.get("description", ""))
    completed = data.get("completed", task["completed"])

    if not title or not isinstance(title, str):
        return jsonify({"error": "Field 'title' must be a non-empty string"}), 400

    # Update fields
    task["title"] = title.strip()
    if isinstance(description, str):
        task["description"] = description.strip()
    task["completed"] = bool(completed)

    # Save updated list
    save_tasks(tasks)

    return jsonify({
        "message": "Task updated successfully",
        "task": task
    }), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """
    Delete a task by ID.
    """
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)

    return jsonify({"message": "Task deleted successfully"}), 200


@app.route("/tasks/reset", methods=["POST"])
def reset_tasks():
    """
    (Optional bonus) Reset all tasks.
    This will clear the JSON file and start with an empty list.
    """
    save_tasks([])
    return jsonify({"message": "All tasks have been reset"}), 200


if __name__ == "__main__":
    # For local development / testing
    app.run(host="0.0.0.0", port=5000, debug=True)
