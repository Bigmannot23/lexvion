import time, os

os.makedirs("reports/retrospectives", exist_ok=True)
report_md = f"# Governance Retrospective Report ({time.strftime('%Y-%m-%d')})\n\n"
report_md += "- Incidents this period: **1**\n- Improvement Actions:\n- [ ] Example: Add better logging\n"

retro_path = f"reports/retrospectives/retro_{time.strftime('%Y%m%d')}.md"
open(retro_path, "w").write(report_md)
with open("CHANGELOG.md", "a") as clog:
    clog.write(f"{time.strftime('%Y-%m-%d')}: Retrospective generated\n")

print("Feedback report generated and changelog updated.")
