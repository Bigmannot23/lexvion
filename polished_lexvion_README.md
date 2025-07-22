
# Lexvion: Audit‑By‑Default Compliance Engine

Lexvion is a trust‑centered compliance stack built for operators who need provable, audit‑ready evidence for every action.  Inspired by modern DevOps and security practices, Lexvion automatically records and bundles all configuration, policy and runtime evidence into timestamped audit packages.

## 🔍 What It Does

* **Evidence logging and bundle signing** – every policy change, configuration update and user action is logged with cryptographic signatures.
* **Self‑serve Trust Center** – a web dashboard lets stakeholders download the latest audit bundle with one click.
* **Configurable privacy policies** – easily toggle data retention, redaction and watermarking via YAML files.
* **Full provenance trail** – audit bundles include logs, configs, policies, reports and badges so your compliance story is complete.

## 🛠 Tech Stack & Architecture

Lexvion is built with Python and FastAPI on the back end and uses simple static HTML/JS for the Trust Center UI.  Cron jobs generate evidence bundles on schedule and Python’s `hashlib` library signs each ZIP archive.  All artifacts live in a version‑controlled repository so nothing is hidden.

High‑level components:

1. **FastAPI service** – exposes endpoints to query audit status and trigger bundle generation.
2. **Bundle generator** – collects logs, config files and policies, packages them into a ZIP and writes a `.sha256` signature file.
3. **Trust Center dashboard** – static site served from `/docs/trust_center_dashboard` with a download button for the latest bundle.
4. **Audit logs & reports** – stored under `/logs`, `/configs`, `/policies` and `/reports`.  These folders can be extended with your own evidence types.

## ✅ Why It Matters

* **Instant compliance proof** – no more scrambling before an audit; the evidence is always up‑to‑date.
* **Cryptographically verifiable** – SHA‑256 signatures prevent tampering and demonstrate integrity.
* **Operator‑ready** – simple CLI and dashboard mean anyone can verify the system works.

Use Lexvion as a template for your own audit‑by‑default systems or fork it to integrate with your SaaS.
