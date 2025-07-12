import streamlit as st
import os
import json
from datetime import datetime
from zipfile import ZipFile
import tempfile
import subprocess

st.set_page_config(page_title="Lexvion Trust Center", layout="wide")

st.title("🛡️ Lexvion Trust Center — Evidence Verifier")

# Status Badge Panel
badge_path = "configs/compliance_status.json"
if os.path.exists(badge_path):
    with open(badge_path) as f:
        badge = json.load(f)
    st.success(f"Compliance Status: {badge.get('status', 'unknown')}")
    st.text(f"Last Verified: {badge.get('last_verified', 'N/A')}")
else:
    st.warning("⚠️ No compliance badge found.")

# Upload + Verify Panel
st.header("📂 Upload Bundle to Verify")
uploaded_file = st.file_uploader("Drop an audit bundle (.zip) here", type="zip")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Verifying...")
    result = subprocess.run(["python", "src/verify_bundle.py", tmp_path], capture_output=True, text=True)

    import json
from datetime import datetime

badge_path = "configs/compliance_status.json"
status = "FAIL"
import json
from datetime import datetime

badge_path = "configs/compliance_status.json"
status = "FAIL"
if "All files verified successfully" in result.stdout:
    st.success("✅ Bundle integrity verified")
    status = "PASS"
else:
    st.error("❌ Bundle failed verification")
    status = "FAIL"
st.code(result.stdout)

# Auto-update badge
badge_update = {
    "log_integrity": status,
    "last_updated": datetime.utcnow().isoformat() + "Z"
}
os.makedirs(os.path.dirname(badge_path), exist_ok=True)
with open(badge_path, "w") as f:
    json.dump(badge_update, f, indent=2)

# Log to verification history
history_path = "logs/verify_history.jsonl"
verdict = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "bundle": uploaded_file.name if uploaded_file else "unknown",
    "status": status,
}
os.makedirs(os.path.dirname(history_path), exist_ok=True)
with open(history_path, "a") as f:
    f.write(json.dumps(verdict) + "\n")

st.experimental_rerun()



# Auto-update the badge!
badge_update = {
    "log_integrity": status,
    "last_updated": datetime.utcnow().isoformat() + "Z"
}
os.makedirs(os.path.dirname(badge_path), exist_ok=True)
with open(badge_path, "w") as f:
    json.dump(badge_update, f, indent=2)

st.experimental_rerun()  # Instantly refreshes the UI with new badge status!

# Download Section
st.header("⬇️ Latest Audit Bundle")
latest = None
bundle_dir = "audit_bundles"
if os.path.exists(bundle_dir):
    files = sorted(os.listdir(bundle_dir), reverse=True)
    for f in files:
        if f.endswith(".zip"):
            latest = os.path.join(bundle_dir, f)
            break

if latest:
    with open(latest, "rb") as f:
        st.download_button(label="Download Latest Bundle", data=f, file_name=os.path.basename(latest))
else:
    st.warning("No bundles found.")
import streamlit as st
# The following block is redundant and duplicates logic above, so it should be removed to avoid errors and confusion.st.header("📖 Log Explorer")

log_path = "logs/incident_log.jsonl"
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        lines = f.readlines()
    st.write(f"Showing last {min(20, len(lines))} log entries:")
    for line in lines[-20:]:
        st.json(json.loads(line))
    with open(log_path, "rb") as f:
        st.download_button("Download Full Log", data=f, file_name="incident_log.jsonl")
else:
    st.warning("No log file found at logs/incident_log.jsonl")
st.header("🕒 Verification History")

history_path = "logs/verify_history.jsonl"
if os.path.exists(history_path):
    with open(history_path, "r") as f:
        records = [json.loads(line) for line in f.readlines()]
    # Show the 10 most recent (most recent at top)
    st.write("Last 10 verifications:")
    for row in records[-10:][::-1]:
        icon = "✅" if row["status"] == "PASS" else "❌"
        st.write(f"{icon} {row['timestamp']} — {row['bundle']} — {row['status']}")
    # Download as CSV
    import pandas as pd
    df = pd.DataFrame(records)
    st.download_button("Download Verification History CSV", data=df.to_csv(index=False), file_name="verify_history.csv")
else:
    st.info("No verification history yet.")
import pandas as pd

st.header("📝 Generate Audit Report")

# Compose audit report data
def generate_audit_report():
    # Load badge
    badge = {}
    if os.path.exists(badge_path):
        with open(badge_path) as f:
            badge = json.load(f)
    # Load history
    history = []
    history_path = "logs/verify_history.jsonl"
    if os.path.exists(history_path):
        with open(history_path) as f:
            history = [json.loads(line) for line in f.readlines()]
    # Load latest bundle manifest (optional)
    manifest = {}
    bundle_dir = "audit_bundles"
    latest_bundle = None
    if os.path.exists(bundle_dir):
        files = sorted(os.listdir(bundle_dir), reverse=True)
        for f_ in files:
            if f_.endswith(".zip"):
                latest_bundle = os.path.join(bundle_dir, f_)
                break
    manifest_text = ""
    if latest_bundle:
        from zipfile import ZipFile
        with ZipFile(latest_bundle, "r") as zipf:
            if "manifest.json" in zipf.namelist():
                manifest_text = zipf.read("manifest.json").decode()
                manifest = json.loads(manifest_text)
    # Compose report
    report = {
        "badge": badge,
        "last_bundle_manifest": manifest,
        "verification_history": history[-10:],  # last 10 for brevity
    }
    return report, manifest_text

report, manifest_text = generate_audit_report()

# Show and download as JSON or CSV
if st.button("Generate Audit Report (JSON)"):
    st.json(report)
    st.download_button("Download Audit Report JSON", data=json.dumps(report, indent=2), file_name="audit_report.json")

if manifest_text:
    st.download_button("Download Manifest JSON", data=manifest_text, file_name="manifest.json")

# Download verification history as CSV
if report["verification_history"]:
    df = pd.DataFrame(report["verification_history"])
    st.download_button("Download Verification History (CSV)", data=df.to_csv(index=False), file_name="verify_history.csv")
