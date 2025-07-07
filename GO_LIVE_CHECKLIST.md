# LEXVION GO-LIVE CHECKLIST (AUDIT-BY-DEFAULT)

## Technical Evidence

- [ ] All outputs signed; every file in `output_watermarking` has a `.sig`
- [ ] All signature verifications PASS (run `verify_file.py` for every output)
- [ ] Audit bundle ZIP created (run `bundle_audit.py`); .sha256 hash file present
- [ ] Bundle includes: output_watermarking, logs, policies, reports, scripts

## Tamper Proofing

- [ ] Tamper test performed (manually edit a signed file, verify signature FAILS)

## Operator Proof

- [ ] Every step above confirmed by operator, with date
- [ ] All scripts (`sign_file.py`, `verify_file.py`, `bundle_audit.py`) present in repo and pass run/test

## Compliance Process

- [ ] Checklist reviewed before launch, with operator sign-off
- [ ] (Optional) README present for onboarding/hand-off

---

**Operator Sign-Off:** ________________________   **Date:** _______________

