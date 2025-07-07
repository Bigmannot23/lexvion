"""Lexvion Operator - Bundle & Export Evidence with SHA256 Manifest"""

import os, zipfile, hashlib, json, logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def create_bundle(log_dir, report_dir, output_path):
    manifest = {
        "bundle_uuid": hashlib.sha256(str(datetime.utcnow()).encode()).hexdigest(),
        "created": datetime.utcnow().isoformat(),
        "files": []
    }

    with zipfile.ZipFile(output_path, 'w') as zipf:
        for folder in [log_dir, report_dir]:
            for file in os.listdir(folder):
                full_path = os.path.join(folder, file)
                file_hash = sha256_file(full_path)
                manifest["files"].append({
                    "name": file,
                    "path": full_path,
                    "sha256": file_hash
                })
                zipf.write(full_path, arcname=file)
                logging.info(f"Added {file} with hash {file_hash}")

        # Write manifest.json
        manifest_path = "manifest.json"
        with open(manifest_path, "w") as mf:
            json.dump(manifest, mf, indent=2)
        zipf.write(manifest_path)
        os.remove(manifest_path)

    logging.info(f"✅ Bundle created at: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Lexvion Bundle Creator")
    parser.add_argument("--logs", required=True)
    parser.add_argument("--reports", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    create_bundle(args.logs, args.reports, args.output)
