import json
import argparse
from datetime import datetime

BADGE_PATH = "configs/compliance_status.json"

def update_badge(log_status):
    badge = {
        "log_integrity": "PASS" if log_status else "FAIL",
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }

    with open(BADGE_PATH, "w") as f:
        json.dump(badge, f, indent=2)

    print(f"[BADGE] Updated badge to {badge['log_integrity']} ✅")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-status", required=True, choices=["pass", "fail"], help="Log verification result")
    args = parser.parse_args()

    update_badge(args.log_status == "pass")
