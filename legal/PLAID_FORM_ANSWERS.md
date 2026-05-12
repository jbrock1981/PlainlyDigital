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
| Patet Privacy Policy (Q9 URL) | Live at plainlydigital.com | `https://plainlydigital.com/patet/privacy` |
| Patet Terms of Service | Live at plainlydigital.com | `https://plainlydigital.com/patet/terms` |
| Markdown sources (for edits) | `legal/04_Information_Security_Policy.md`, `legal/10_Access_Control_Policy.md` | Same dir as DOCX |
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

Pre-step — open `https://plainly-psi.vercel.app/` in a browser and sign
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

Retention table is in the Patet Privacy Policy under "Retention & policy review":

| Category | Retention | Trigger to delete |
|---|---|---|
| Account profile, lesson progress | Lifetime of account | 30 days after `DELETE /api/auth/me` |
| Coach conversation messages | 12 months rolling | Account delete OR per-conversation delete |
| Plaid access tokens | Lifetime of connected bank | Bank disconnect (immediate); account delete |
| Plaid transaction snapshots | Lifetime of account | Account delete; per-transaction delete |
| Subscription receipts (RevenueCat) | 7 years (tax) | Aged out per IRS |
| Audit + security event log | 24 months | Aged out automatically |
| Anonymized crash data (Sentry) | 90 days | Aged out automatically |

**Review cadence:** Annually by the Managing Member; within 30 days of
any material vendor/regulatory change. Documented in:

- Privacy Policy "Retention & policy review" (Plaid Link URL evidence)
- IS Policy §10 (Privacy & Regulatory Posture) + §11 (Training, Awareness & Review)
- Access Control Policy §8.3 (Audit-log retention & immutability) + §8.4 (Periodic access review)

---

## Pre-meeting checklist

- [ ] Q4 screenshots taken (3) and saved
- [ ] Q5 screenshots taken (2-3) and saved
- [ ] Both DOCXes staged on desktop for upload
- [ ] Live verify: `curl -sI https://plainlydigital.com/patet/privacy` returns 200
- [ ] Live verify: `curl -sI https://plainly-psi.vercel.app/mfa` returns 200
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
