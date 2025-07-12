import hashlib
import os

def sha256_file(path):
    """Compute SHA-256 hash of a file."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def merkle_hash(file_hashes):
    """Compute Merkle root from a sorted list of hex hashes (as strings)."""
    if not file_hashes:
        return None
    current_level = sorted(file_hashes)
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i+1 < len(current_level) else left
            next_level.append(hashlib.sha256((left + right).encode()).hexdigest())
        current_level = next_level
    return current_level[0]

if __name__ == "__main__":
    log_file = "logs/incident_log.jsonl"
    if not os.path.exists(log_file):
        print(f"[ERROR] File not found: {log_file}")
    else:
        file_hashes = [sha256_file(log_file)]
        root = merkle_hash(file_hashes)
        print(f"[DEBUG] Merkle Root of {log_file}: {root}")
import json
from datetime import datetime

def build_manifest(file_paths, output_path="bundles/manifest.json"):
    manifest = {
        "files": [],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    file_hashes = []
    for path in file_paths:
        if os.path.exists(path):
            file_hash = sha256_file(path)
            file_hashes.append(file_hash)
            manifest["files"].append({
                "filename": path,
                "hash": file_hash
            })
        else:
            print(f"[WARN] File not found: {path}")

    merkle_root = merkle_hash(file_hashes)
    manifest["merkle_root"] = merkle_root

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[✅] Manifest written to {output_path} with Merkle root: {merkle_root}")
if __name__ == "__main__":
    files_to_bundle = [
        "logs/incident_log.jsonl",
        "configs/public_key.pem",
        "configs/compliance_status.json"
    ]
    build_manifest(files_to_bundle)
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from zipfile import ZipFile
import time

def sign_data(data: bytes, key_path="configs/private_key.pem") -> str:
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    return private_key.sign(data).hex()

def create_signed_bundle(files, manifest_path="bundles/manifest.json"):
    # Read manifest and Merkle root
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    root_hash = manifest["merkle_root"]
    
    # Sign the Merkle root
    signature = sign_data(bytes.fromhex(root_hash))
    manifest["signature"] = signature
    manifest["signed_at"] = datetime.utcnow().isoformat() + "Z"

    # Overwrite manifest with signature
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Bundle everything into ZIP
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    zip_name = f"audit_bundle_{ts}.zip"
    zip_path = os.path.join("audit_bundles", zip_name)
    os.makedirs("audit_bundles", exist_ok=True)

    with ZipFile(zip_path, "w") as zipf:
        for f in files + [manifest_path]:
            zipf.write(f, arcname=os.path.basename(f))
    
    print(f"[✅] Audit bundle written: {zip_path}")


