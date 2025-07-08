## 🚦 Audit Evidence Operator Guide (How to Prove This System Is Real)

> 🗣️ *“Even though it’s above my head, lol — you’re a high-agency individual. Creating value.”*  
> — **Erik Burgess**, LinkedIn

**To validate the Lexvion Trust Center’s audit-by-default evidence pipeline:**

1. **Go to the Trust Center dashboard in your browser.**
   - URL: `http://127.0.0.1:5500/docs/trust_center_dashboard/index.html`

2. **Click the “Download Latest Audit Bundle” button.**
   - This downloads the current timestamped audit evidence `.zip` file from `/audit_bundles/`.

3. **Open or extract the ZIP file using Windows File Explorer or 7-Zip.**
   - Inside you’ll find all compliance evidence:  
     - `/logs` (incident logs, lineage, etc.)
     - `/configs` (privacy, watermarking, lineage configs)
     - `/policies` (all active policy docs)
     - `/reports` (drill reports, feedback, retros)
     - `/badges` (live compliance status)

4. **Verify the bundle’s integrity (optional, advanced):**
   - Compare the `.sha256` file with the ZIP using:
     ```
     certutil -hashfile <zipfilename> sha256
     ```
     The output hash should match the string in the `.sha256` file.

5. **(Optional) Check each evidence file:**
   - Open logs, configs, or reports as needed—everything is readable, timestamped, and exportable.

---

**This is the single source of truth for all audit, compliance, and trust proof. Every bundle is produced automatically. Nothing is hidden.**

*Last audit bundle generated: [version 1]*



