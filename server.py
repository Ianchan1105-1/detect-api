from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = "detect.db"

def get_latest_record():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT detected_number, timestamp FROM detected_numbers ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "detected_number": row[0],
            "timestamp": row[1]
        }
    else:
        return {
            "detected_number": "無資料",
            "timestamp": "無資料"
        }

@app.route("/update", methods=["POST"])
def update_data():
    data = request.get_json()

    number = data.get("detected_number")
    ts = data.get("timestamp")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO detected_numbers (detected_number, timestamp) VALUES (?, ?)",
              (number, ts))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(get_latest_record())

