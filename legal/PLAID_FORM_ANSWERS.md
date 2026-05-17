# Plaid due-diligence form — answer reference

**Prepared:** 2026-05-12 for the Patet × Plaid account-setup meeting.
**Status:** All evidence shipped + verified. Server live on Render; web bundle live on Vercel; both Neon migrations applied to prod; both DOCX uploads regenerated tonight.

This file is the single place to look while filling out the form. It's
not deployed publicly — it lives in the repo only.

---

## File / URL inventory

| Need | Source | Path |
|---|---|---|
| InfoSec Policy DOCX | `legal/04_Information_Security_Policy.docx` | `/home/jbroc/repos/PlainlyDigital/legal/04_Information_Security_Policy.docx` |
| Access Control Policy DOCX | `legal/10_Access_Control_Policy.docx` | `/home/jbroc/repos/PlainlyDigital/legal/10_Access_Control_Policy.docx` |
| Data Retention and Disposal Policy DOCX (Q11 attachment) | `legal/11_Data_Retention_and_Disposal_Policy.docx` | `/home/jbroc/repos/PlainlyDigital/legal/11_Data_Retention_and_Disposal_Policy.docx` |
| Patet Privacy Policy (Q9 URL) | Live at plainlydigital.com | `https://plainlydigital.com/patet/privacy` |
| Patet Terms of Service | Live at plainlydigital.com | `https://plainlydigital.com/patet/terms` |
| Markdown sources (for edits) | `legal/04_Information_Security_Policy.md`, `legal/10_Access_Control_Policy.md`, `legal/11_Data_Retention_and_Disposal_Policy.md` | Same dir as DOCX |
| DOCX regenerator (if any md edit needed) | `legal/generate_infosec_policy.py` | `/tmp/docxenv/bin/python legal/generate_infosec_policy.py <file.md>` |

---

## Q1-Q3 — Information Security

The form asks whether Plainly Digital has a documented, operationalized
information security policy. **Answer: Yes**, upload
`legal/04_Information_Security_Policy.docx` if they want the full file.

Covers identification of risks, vendor inventory with SOC 2 status,
incident response (4-level scale + 72-hour breach notice), data
classification (4 tiers), encryption standards in transit + at rest,
change management, operational controls, privacy + regulatory posture,
training cadence, and annual review.

---

## Q4 — MFA before Plaid Link is surfaced (consumers, mobile/web)

**Answer: Yes.** Backed by Patet migration 023 + `server/src/lib/mfa.ts`.
`POST /api/plaid/link-token` returns `403 mfa_required` when no MFA is on
the account, or `403 mfa_step_up_required` when the most recent challenge
is older than 5 minutes. The client routes the user to `/mfa/setup` or
`/mfa/challenge` and replays Plaid Link after success.

**Doc evidence:** Access Control Policy §4.1.

**Screenshots needed (3, take from web bundle):**

Pre-step — open `https://patet.plainlydigital.com/` in a browser and sign
in to a test account (no MFA on it yet).

1. **Profile → "🔐 Two-factor authentication" row.**
   Proves the MFA entry point is a first-class user-facing setting.
2. **`/mfa/setup` after tapping "Begin setup".**
   Shows the QR code (220×220), the manual entry secret, and the 6-digit
   verify field. Proves the actual MFA pairing UI.
3. **`/plaid/connect` immediately bouncing to `/mfa/setup`.**
   With MFA OFF, opening Connect-bank surfaces the gate. Proves
   enforcement *before* Plaid Link reaches the user.

Optional 4th: after completing pairing with Google Authenticator,
screenshot the recovery-codes display.

---

## Q5 — MFA on critical systems holding consumer financial data

**Answer: Yes.** Hardware-key (FIDO2/WebAuthn) MFA on every vendor
console held by the Managing Member. The application-side `role='admin'`
and `role='support'` identities inherit MFA through the same TOTP system
used for consumers.

**Doc evidence:** Access Control Policy §4.2.

**Screenshots needed (pick 2-3 from your vendor consoles):**

- **Google Workspace 2-Step Verification** — `myaccount.google.com/signinoptions/two-step-verification`. Shows hardware keys and/or TOTP enrolled.
- **GitHub two-factor** — `github.com/settings/security`. Shows TOTP or security key on `jbrock1981`.
- **Render 2FA** — Render dashboard → Account Settings → Security. Shows TOTP enabled.
- **Apple ID 2FA** — `appleid.apple.com` → Sign-In & Security. Shows trusted devices list.
- **Neon 2FA** — Neon account settings → Security (turn on tonight if not already).

Three is generally enough; aim for breadth across hosting (Render) +
source control (GitHub) + identity provider (Google).

---

## Q6 — TLS 1.2+ for data in transit

**Answer: Yes.** TLS 1.2 minimum, TLS 1.3 preferred. Every public
endpoint is HTTPS-only with HSTS (`max-age=31536000; includeSubDomains; preload`).
Marketing site cert from Google Trust Services (Firebase Hosting).
API tier (Render) and web bundle (Vercel) terminate TLS at the
provider edge.

**Doc evidence:** IS Policy §5 + Access Control Policy §9.

---

## Q7 — Encrypt consumer data received from Plaid at rest

**Answer: Yes.** AES-256-GCM at the application layer.

- Plaid access tokens encrypted via `server/src/lib/crypto.ts`.
- Financial-snapshot + debt-balance columns encrypted via the same
  primitive (Patet migration 017 Phase A).
- Disk-level encryption at Neon (SOC 2 Type 2) is treated as a second
  layer, not the authoritative control.

**Doc evidence:** IS Policy §3 (data classification — Financial / Restricted
tier) + §5 (Encryption Standards) + Access Control Policy §5.2.

---

## Q8 — Vulnerability management on machines + production assets

**Answer: Partial.** Select what's true; don't oversell.

Honest box selection:

- ✅ **Automated dependency scanning in CI.** `npm audit --audit-level=high`
  blocks deploys on high/critical findings; both Patet server and the
  marketing site repo run this.
- ✅ **Endpoint encryption + automatic security updates** on the
  Managing Member's primary devices (full-disk encryption,
  auto-update).
- ✅ **Provider-managed infrastructure patching.** Render / Vercel /
  GCP / Neon all run hosted infra; we don't manage VMs or kernels
  directly.
- ❌ **Dedicated endpoint vulnerability scanner** (e.g., CrowdStrike,
  SentinelOne) — not in place. Appropriate to single-founder posture.
- ❌ **Container/image scanning** (e.g., Trivy, Snyk Container) — not in
  place today; will land when Patet migrates to GCP Cloud Run with
  Artifact Registry + Container Analysis.
- ❌ **External penetration test** — not yet; planned post-revenue
  ($5K MRR threshold).

**Doc evidence:** IS Policy §8 (Change Management & Secure Development).

---

## Q9 — Privacy policy URL for the app where Plaid Link will be deployed

**Answer: Yes.** Link: `https://plainlydigital.com/patet/privacy`

Confirm the live page shows the updated tonight content before submitting:
```bash
curl -s https://plainlydigital.com/patet/privacy | grep "How we obtain your consent"
```
Should return a match. If not, Vercel/Firebase Hosting hasn't redeployed
the latest commit yet — wait 1-2 min and retry.

---

## Q10 — Consent for collection, processing, storage

**Answer: Yes.**

- Registration screen gates account creation on explicit ToS + Privacy
  Policy acceptance. No data is collected before that consent.
- Bank connection: Plaid's own consent UI inside Plaid Link surfaces
  before any bank credentials are entered; user can decline.
- AI-coach disclosure: every reply is tagged with the AIBadge so the
  user understands they're talking to an AI.
- Right to withdraw consent: account deletion (`DELETE /api/auth/me`)
  cascades all per-user data.

**Doc evidence:** Patet Privacy Policy "How we obtain your consent"
section (added 2026-05-12) + IS Policy §10.

---

## Q11 — Data retention + deletion policy, reviewed periodically

**Answer: Yes.**

**Document to upload:** `legal/11_Data_Retention_and_Disposal_Policy.docx`

The dedicated policy document was added 2026-05-17 specifically to satisfy this question's "Please provide your Data Retention and Disposal Policy" attachment requirement. It is canonical for the retention and disposal of personal and operational data across every Plainly Digital product.

Headline contents:
- §1 Purpose & Scope — implements GDPR Art. 5(1)(e), GDPR Art. 17, CCPA/CPRA §1798.105
- §2 Principles — storage limitation, trigger-based deletion, erasure on request, disposal at the database layer, periodic review
- §3 Retention schedule (exhaustive table covering 19 data categories with retention period, deletion triggers, storage location, disposal method)
- §3.1 Legal-retention carve-outs (tax, fraud investigations, legal hold)
- §4 Third-party processors (Neon, Render, Vercel, Plaid, RevenueCat, Anthropic, Resend, Sentry)
- §5 Backups (7-day Neon backup window + EDPB Guidelines 06/2020 alignment)
- §6 Disposal mechanisms (CASCADE delete, application-layer encryption, anonymization, scheduled purge jobs)
- §7 User rights & self-service (export, delete, correct, disconnect bank, portability, COPPA)
- §8 Vendor incident response (72-hour GDPR Art. 33 notification)
- §9 Periodic review (annual + within-30-days-of-material-change + within-24-hours-of-incident)
- §10 Revision history

**Companion documents** (referenced for cross-validation; not required as primary attachments):

- Patet Privacy Policy "Retention & policy review" section — `https://plainlydigital.com/patet/privacy`
- IS Policy §10 (Privacy & Regulatory Posture) + §11 (Training, Awareness & Review)
- Access Control Policy §8.3 (Audit-log retention & immutability) + §8.4 (Periodic access review)

---

## Pre-meeting checklist

- [ ] Q4 screenshots taken (3) and saved
- [ ] Q5 screenshots taken (2-3) and saved
- [ ] Both DOCXes staged on desktop for upload
- [ ] Live verify: `curl -sI https://plainlydigital.com/patet/privacy` returns 200
- [ ] Live verify: `curl -sI https://patet.plainlydigital.com/mfa` returns 200
- [ ] Live verify: `curl -sI https://plainly-c8jw.onrender.com/api/health` returns 200

---

## What is honest "No" on this form

Do not claim:

- Automated SCIM-based de-provisioning
- Zero-trust network architecture
- Centralized enterprise IAM platform
- Dedicated endpoint detection & response (EDR) on every device
- External penetration testing
- Bug bounty program
- Formal SOC 2 / ISO 27001 certification

These are honest "not yet" answers appropriate to a Year-1 solo-founder
LLC. The Access Control Policy §3.2 explicitly documents the automated-
deprovisioning gap and the headcount-≥3 trigger for revisiting.
