import json, time, os

log_entry = {
    "timestamp": time.time(),
    "scenario": "Prompt Injection",
    "result": "Simulated attack detected and handled",
    "operators_notified": True
}

os.makedirs("logs", exist_ok=True)
with open("logs/incident_log.json", "a") as f:
    f.write(json.dumps(log_entry) + "\n")

print("Red-team drill simulated. Incident logged.")
