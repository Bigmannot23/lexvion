from flask import Flask, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

LOG_FILE = "logs/incident_log.json"

@app.route('/api/run_drill', methods=['POST'])
def run_drill():
    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "scenario": "Red team drill (dashboard trigger)",
        "outcome": "Simulated via Trust Center"
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []
    log.append(event)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)
    return jsonify({"status": "ok", "event": event})

if __name__ == "__main__":
    app.run(port=5050, debug=True)


