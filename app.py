from flask import Flask, render_template, request, jsonify
import os
import csv
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "attendance.csv"
TEMPLATE_FOLDER = "templates"

# Ensure the templates folder exists
if not os.path.exists(TEMPLATE_FOLDER):
    os.makedirs(TEMPLATE_FOLDER)
    with open(os.path.join(TEMPLATE_FOLDER, "index.html"), "w") as f:
        f.write("<h1>Attendance System</h1>")

# Ensure CSV file has a header
def initialize_csv():
    try:
        with open(CSV_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Student ID", "Action"])
    except FileExistsError:
        pass

initialize_csv()  

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_attendance():
    data = request.get_json()
    print("Received data:", data)  # Debug print to see what's being received
    
    # Accept both student_id and worker_id field names for compatibility
    student_id = data.get('student_id', data.get('worker_id', '')).strip()
    action = data.get('action', '').strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if student_id and action in ['Entrance', 'Exit']:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, student_id, action])
        return jsonify({"status": "success"})
    else:
        # More detailed error message for debugging
        error_msg = []
        if not student_id:
            error_msg.append("Missing student ID")
        if not action or action not in ['Entrance', 'Exit']:
            error_msg.append(f"Invalid action: '{action}' (must be 'Entrance' or 'Exit')")
            
        return jsonify({
            "status": "error", 
            "message": "Invalid data: " + ", ".join(error_msg)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1453, debug=True)
