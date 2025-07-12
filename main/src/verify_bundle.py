from zipfile import ZipFile
import hashlib
all_pass = True

def sha256_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def verify_bundle(bundle_path):
    if not os.path.exists(bundle_path):
        print(f"[ERROR] Bundle file not found: {bundle_path}")
        return

    with ZipFile(bundle_path, "r") as zipf:
        file_list = zipf.namelist()
        if "manifest.json" not in file_list:
            print("[ERROR] No manifest.json found in bundle.")
            return

        zipf.extract("manifest.json", path="temp_bundle")

    with open("temp_bundle/manifest.json") as f:
        manifest = json.load(f)

    print(f"[DEBUG] Manifest files: {[f['filename'] for f in manifest['files']]}")
# Verify each file in the manifest
import zipfile, hashlib, json, os, sys

def sha256_file(fileobj):
    h = hashlib.sha256()
    while chunk := fileobj.read(8192):
        h.update(chunk)
    return h.hexdigest()

def merkle_hash(hash_list):
    if not hash_list:
        return None
    current_level = sorted(hash_list)
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i+1] if i+1 < len(current_level) else left
            next_level.append(hashlib.sha256((left + right).encode()).hexdigest())
        current_level = next_level
    return current_level[0]

def verify_bundle(zip_path):
    if not os.path.exists(zip_path):
        print(f"[ERROR] Bundle not found: {zip_path}")
        return False

    with zipfile.ZipFile(zip_path, 'r') as zf:
        if 'manifest.json' not in zf.namelist():
            print("[❌] Manifest missing from bundle.")
            return False

        manifest = json.loads(zf.read('manifest.json'))

        hash_errors = []
        computed_hashes = []

        for file in manifest["files"]:
            name = file["filename"]
            expected = file["hash"]
            if name not in zf.namelist():
                hash_errors.append(f"[MISSING] {name}")
                continue
            actual = sha256_file(zf.open(name))
            computed_hashes.append(actual)
            if actual != expected:
                hash_errors.append(f"[HASH MISMATCH] {name} → expected {expected[:10]}..., got {actual[:10]}...")

        computed_root = merkle_hash(computed_hashes)
        stored_root = manifest["merkle_root"]

        if computed_root != stored_root:
            print(f"[❌] Merkle root mismatch.\nExpected: {stored_root}\nGot:      {computed_root}")
            return False

        if hash_errors:
            print(f"[❌] {len(hash_errors)} issues found in bundle:")
            for e in hash_errors:
                print("   ", e)
            return False

        print("[✅] Bundle passed verification. All hashes + Merkle root match.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_bundle.py <path_to_bundle.zip>")
        sys.exit(1)

    verify_bundle(sys.argv[1])
# Example usage:
# python verify_bundle.py bundles/incident_bundle.zip
       # Wrap up verification
    if all_pass:
        print("[✅] All files verified successfully.")
    else:
        print("[❌] Some files failed verification.")
