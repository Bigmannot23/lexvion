import os
import json
import base64
import hashlib
import argparse
import datetime
import secrets

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

# === Paths ===
LOG_PATH = os.path.join(os.path.dirname(__file__), '../../logs/incident_log.jsonl')
KEY_PATH = os.path.join(os.path.dirname(__file__), '../../configs/private_key.pem')

# === Hashing Utilities ===
def sha3_256(data: bytes) -> str:
    """Return SHA3-256 hash as hex string"""
    return hashlib.sha3_256(data).hexdigest()

def load_ed25519_private_key(path: str):
    """Load Ed25519 private key from PEM"""
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def sign_entry(entry_hash_hex: str, private_key) -> str:
    """Sign the hash of an entry using Ed25519"""
    hash_bytes = bytes.fromhex(entry_hash_hex)
    signature = private_key.sign(hash_bytes)
    return base64.b64encode(signature).decode()

def get_last_log_entry():
    """Retrieve last entry and index, or return (None, -1)"""
    if not os.path.exists(LOG_PATH):
        return None, -1
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            return None, -1
        last = json.loads(lines[-1])
        return last, last.get("log_index", -1)

def append_log_entry(event_type: str, actor: str, details: str):
    """Append a cryptographically linked log entry"""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    last_entry, last_index = get_last_log_entry()
    prev_hash = last_entry["entry_hash"] if last_entry else "0" * 64

    entry = {
        "log_index": last_index + 1,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "actor": actor,
        "details": details,
        "prev_hash": prev_hash,
        "nonce": secrets.randbits(64),
    }

    hash_input = json.dumps(entry, sort_keys=True).encode("utf-8")
    entry_hash = sha3_256(hash_input)
    entry["entry_hash"] = entry_hash

    try:
        private_key = load_ed25519_private_key(KEY_PATH)
        entry["signature"] = sign_entry(entry_hash, private_key)
    except Exception as e:
        entry["signature"] = None
        print(f"[WARN] Could not sign log entry: {e}")

    if last_entry:
        expected = last_entry["entry_hash"]
        if prev_hash != expected:
            raise RuntimeError(f"[ERROR] Chain break: expected prev_hash={expected}, got {prev_hash}")

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"[OK] Appended log #{entry['log_index']} with hash={entry_hash[:10]}...")

# === CLI Runner ===
def main():
    parser = argparse.ArgumentParser(description="Lexvion: Log + Sign CLI")
    parser.add_argument("--event", required=True, help="Event type (e.g., model_update)")
    parser.add_argument("--actor", required=True, help="Email or system ID")
    parser.add_argument("--details", required=True, help="Description of event")
    args = parser.parse_args()

    append_log_entry(args.event, args.actor, args.details)

if __name__ == "__main__":
    main()
