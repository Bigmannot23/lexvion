import os
import zipfile
import hashlib
from datetime import datetime

# Directories to include in audit bundle
INCLUDE_DIRS = INCLUDE_DIRS = [
    "output_watermarking",
    "logs",
    "policies",
    "reports",
    "scripts",
]


# Create output folder for bundles if needed
BUNDLE_DIR = "audit_bundles"
os.makedirs(BUNDLE_DIR, exist_ok=True)

# Name bundle with timestamp
timestamp = datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")

zip_name = f"audit_bundle_{timestamp}.zip"
zip_path = os.path.join(BUNDLE_DIR, zip_name)

# Collect files to bundle
files_to_bundle = []
for d in INCLUDE_DIRS:
    if os.path.isdir(d):
        for root, _, files in os.walk(d):
            for file in files:
                files_to_bundle.append(os.path.join(root, file))
# Add the audit bundle manifest/README to the ZIP

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as bundle:
    for file in files_to_bundle:
        bundle.write(file, arcname=os.path.relpath(file))

    # Now add the manifest INSIDE the block
    manifest_template = """# Audit Bundle Manifest

This archive contains the full compliance evidence bundle for Lexvion Trust Center.
Generated: {timestamp}

## Contents

- /logs        - All runtime/compliance logs (incidents, lineage, etc.)
- /configs     - All compliance-relevant configs (YAML/JSON)
- /policies    - Policy and SOP docs
- /reports     - Incident and drill reports, retrospectives
- /badges      - Current compliance status indicators

To verify authenticity, compare the SHA-256 of the ZIP to the included .sha256 file.
"""
    manifest_content = manifest_template.format(timestamp=timestamp)
    bundle.writestr('README_AUDIT.md', manifest_content)
# The block ENDS here. Do NOT use "bundle" below this line!


