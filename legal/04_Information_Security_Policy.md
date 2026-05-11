# Plainly Digital LLC — Information Security Policy

**Document version:** 1.0
**Effective date:** 2026-05-11
**Owner:** Jonathan Brock, Managing Member (Plainly Digital LLC)
**Review cadence:** Annual (next scheduled review: 2027-05-11), or within 30 days of a material change to systems, vendors, or applicable law.
**Governing law:** Tennessee, USA.

---

## 1. Purpose & Scope

This policy defines how Plainly Digital LLC ("Plainly Digital," "the Company") identifies, mitigates, and monitors information-security risk relevant to its business. It applies to every system, vendor, employee, and contractor that handles Plainly Digital customer data, financial data, or production infrastructure across the Company's products:

- **Patet** — personal-finance literacy app (consumer)
- **Vinla** — personal wellness app (consumer)
- **Winlet** — wins/anti-streak tracker (consumer)
- **Glyphe** — AI life-advisor app (consumer) and the AI-coach personality embedded in each of the above
- **CastFreely**, **Tradingly**, **Fraus**, **Salvis**, **ClearDoc**, **SitterSheet** — additional products under the same controls baseline
- The marketing site at `https://plainlydigital.com`

The policy applies regardless of where data is stored (Neon Postgres, Cloud SQL, Firebase, Vercel, Render, GCP, third-party SaaS) and regardless of whether the data is at rest, in transit, or in processing.

## 2. Roles & Responsibilities

| Role | Held by | Responsibilities |
|---|---|---|
| Managing Member / Security Officer | Jonathan Brock | Final approval of this policy; risk-acceptance decisions; incident-response decision authority; vendor-onboarding sign-off. |
| Engineering | Jonathan Brock (solo founder) | Implement controls; review code; respond to incidents; maintain audit logs. |
| Successor Managing Member | Designated spouse (per LLC Operating Agreement §6.4) | Assumes Managing Member duties on incapacity per the operating agreement. |
| Customers | App users | Use strong, unique passwords; report suspected security issues to `security@plainlydigital.com`. |

Because Plainly Digital is a solo-founder LLC, the Managing Member fulfills the "CISO equivalent" responsibilities. Any future hire whose role touches production or customer data inherits the responsibilities in §3-§11 of this policy on their first day and is required to acknowledge it in writing.

## 3. Data Classification & Handling

The Company classifies data into four tiers. Controls in this policy reference these tiers by name.

| Class | Description | Examples | Required controls |
|---|---|---|---|
| **Public** | Information intended for public consumption. | Marketing copy, lesson curriculum, lesson titles, blog posts. | None beyond integrity (no tampering). |
| **Internal** | Operational data with no direct customer or financial value. | Internal Jira-style task lists, code comments, infrastructure diagrams. | Access limited to authorized personnel. |
| **Confidential** | Customer-identifying or behavior data. | User name, email, lesson progress, push tokens, IP addresses, device fingerprints. | TLS 1.2+ in transit. Access logged. Removed on account deletion (CCPA/GDPR right-to-erasure). |
| **Financial / Restricted** | Money values, account identifiers, government IDs, secrets. | Take-home pay, debt balances, Plaid access tokens, OAuth refresh tokens, API keys, JWT secrets, encryption keys, FICO scores. | AES-256-GCM application-layer encryption at rest in addition to disk-level encryption. Never logged in plaintext. Never displayed in admin UIs without explicit per-row reason. Subject to data-export bundle on user request (CCPA/GDPR Article 15). |

A user data-export bundle (`GET /api/auth/me/export` in Patet) returns the full per-user dataset as a `Content-Disposition: attachment` JSON file with secrets stripped (password hash, Plaid tokens, active reset tokens, internal admin tables) for regulatory compliance.

## 4. Access Control

- **Authentication.** Customer access to Plainly Digital products is via (a) email + password (bcrypt-hashed at cost 10 minimum) or (b) Google OAuth / Apple Sign-In (JWKS-verified). Internal admin endpoints require a server-side `INTERNAL_API_KEY` header rotated at least annually and on any suspected exposure.
- **Authorization.** Sessions are issued as JWTs with a random `jti` claim. Logout and refresh both write the old `jti` to a `revoked_tokens` table; every request middleware-checks the table. Web sessions use httpOnly `SameSite=Strict; Secure` cookies (audit M-tier H1 closed 2026-05); mobile clients use the `Authorization` header.
- **Account lockout.** Failed-login counters are persisted in an `account_lockout` table (Patet migration 015 / equivalents across products) so they survive process restarts. Lockout thresholds: 10 failed attempts → 15-minute cooldown. Login timing is equalized to prevent email enumeration.
- **Multi-factor authentication.** MFA is on the active product roadmap (audit deferred item L10) and will be required before connecting any Plaid bank account on consumer products that integrate Plaid.
- **Least privilege.** Production database access is limited to the Managing Member and to the deployed Render / Cloud Run service accounts via short-lived connection strings. Local developer access uses read-only roles where supported.
- **Secret management.** Production secrets are stored as encrypted environment variables on Render and GCP (never committed to git). The `.gitignore` baseline excludes `.env`, `.env.*`, `server/.env*`, and `.firebase/`. Discovery of a leaked secret triggers immediate rotation (see §7) and a 24-hour incident review.
- **Off-boarding.** On contractor or future-employee off-boarding, all access tokens, deploy keys, and admin credentials they hold are revoked within 24 hours. The Managing Member maintains the access-ownership inventory.

## 5. Encryption Standards

- **In transit.** TLS 1.2+ is required end-to-end. All public endpoints (marketing site, app APIs, webhook receivers) are HTTPS-only with HSTS enabled. Internal service-to-service communication on GCP uses Google-managed certificates.
- **At rest, disk level.** All managed databases (Neon Postgres, Cloud SQL, Firebase Firestore, Supabase Postgres) use the provider's at-rest encryption by default (AES-256). Disk-level encryption alone is not relied on as the sole control for Financial / Restricted data.
- **At rest, application layer.** Financial / Restricted columns are encrypted at the application layer with AES-256-GCM. Keys are stored in environment variables on Render / Cloud Run and rotated on a documented schedule (next rotation: 2026-08-11). The Plaid access-token vault has used this scheme since product launch; financial-snapshot and debt-balance columns were extended to the same scheme in Patet migration 017 (2026-05-10, "PII Phase A"). A scheduled future migration drops the plaintext companion columns after backfill verification.
- **In memory.** Application code avoids logging Restricted data. Logger middleware redacts known field names; engineering review checks new endpoints for accidental Restricted exposure before merge.
- **Backups.** Database backups inherit the provider's encryption-at-rest. Plainly Digital does not export raw backups to long-term storage; restores use the provider's point-in-time recovery.

## 6. Vendor / Third-Party Risk

Before integrating a new vendor that will receive Confidential or Financial / Restricted data, the Managing Member documents:

1. The data classification the vendor will hold.
2. The vendor's SOC 2 / ISO 27001 / similar attestation, or the absence of one and the compensating reason.
3. Whether the vendor signs a Data Processing Agreement (DPA) where applicable.
4. The breach-notification SLA in the vendor contract.

Current critical vendors and their classification scope:

| Vendor | Data held | Attestation | Notes |
|---|---|---|---|
| Plaid | Financial bank-account data, transactions | SOC 2 Type 2 | DPA in place. Access tokens encrypted at rest with AES-256-GCM. Read-only product scope (Transactions / Recurring / Balance) for current consumer apps. |
| Neon (Postgres) | Confidential + Financial / Restricted | SOC 2 Type 2 | Disk-level encryption + application-layer encryption on the columns listed in §5. |
| Render | Confidential + secrets | SOC 2 Type 2 | Encrypted env-var storage; production database connection strings live here. |
| Vercel | Public + Confidential | SOC 2 Type 2 | Hosts marketing site + web exports. No Financial / Restricted data. |
| Firebase Hosting / GCP | Public + Confidential | ISO 27001 / SOC 2 | LLC's `plainlydigital-www` project + the Glyphe app production stack. |
| RevenueCat | Subscription billing metadata | SOC 2 Type 2 | Receives store purchase events. No direct payment-card data — handled by Apple / Google. |
| Anthropic (Claude API) | Conversation content with the AI coach | SOC 2 Type 2 | No persistent training on customer data per Anthropic's commercial terms. |

Vendors are re-reviewed annually as part of the policy review cycle. A vendor losing its attestation triggers a 30-day review and decision (continue / replace / drop the integration).

## 7. Incident Response

Plainly Digital classifies incidents on a four-level scale:

| Level | Definition | Initial response time |
|---|---|---|
| **0 — Confirmed breach** | Confirmed unauthorized access to Financial / Restricted data, OR ≥500 user records of Confidential data. | Within 1 hour. |
| **1 — Suspected breach** | Credible signal of unauthorized access pending confirmation. | Within 4 hours. |
| **2 — Operational** | Service degradation or outage with no confirmed data exposure. | Within 24 hours. |
| **3 — Hygiene** | Detected leaked secret, expired cert warning, anomalous-but-benign access pattern. | Within 7 days. |

**Response steps for Level 0 / 1:**

1. The Managing Member is paged and assumes incident-commander role.
2. Containment: rotate affected secrets; revoke compromised tokens (`jti` revocation table); cut off compromised service accounts.
3. Investigation: pull audit logs (`audit_event_log`, NIST AI RMF logs, infrastructure access logs); preserve timeline and scope.
4. Notification: customers whose Confidential or Financial / Restricted data was accessed are notified by email within 72 hours of confirmation (GDPR Article 33; equivalent US state laws including TN Code §47-18-2107). Plaid, the affected business partners, and any required regulators are notified per contract / law.
5. Remediation: root cause documented; the failing control is strengthened; a post-incident review report is filed in the internal incident log within 14 days.

**Reporting channel.** External security reports come in via `security@plainlydigital.com` and the `.well-known/security.txt` file on the marketing site. The Managing Member triages within 2 business days.

**Rotation events.** Any session in which a production secret is suspected of exposure triggers an immediate rotation cycle: Anthropic API key, JWT secret, encryption key, internal API key, Plaid client/secret, Neon DB password. The 2026-05-09 secret-rotation pass (Patet) is the operational reference for this procedure.

## 8. Change Management & Secure Development

- **Source control.** All production code lives in git on GitHub under `jbrock1981/<repo>`. All work goes to `main` (no long-lived feature branches for solo-founder workflow). Force-pushes to `main` are not used. Pre-commit hooks enforce a clean build (`tsc --noEmit`, `npm test`, build) on the marketing site repo; equivalent gates exist per product.
- **Code review.** Until the Company hires a second engineer, the Managing Member performs self-review with a mandatory cool-off window (no commit-then-push during the same hour for changes touching authentication, payment, or PII paths). External pull requests (none today; reserved for future) require two-party approval.
- **Dependency management.** `npm audit --audit-level=high` runs in CI. High and critical findings block deploy until resolved. Dependency upgrades are reviewed on a quarterly cadence at minimum; security patches are applied immediately.
- **Testing baseline.** Every product carries a server test suite (>300 tests for Patet) and an app test suite. Code reaching production must pass `tsc --noEmit` and the full Jest suite. Contract tests on auth, payments, and PII paths are required for any change to those surfaces.
- **AI governance.** Every AI-backed feature follows the three-layer Glyphe architecture (shared personality / per-app domain / per-user personalization) and the NIST AI Risk Management Framework documented in `Patet/docs/NIST-AI-GOVERNANCE.md`. Crisis-safety language and 211/988 escalation rules are invariant across all persona overlays and cannot be stripped by a persona switch.
- **Deployment.** Cloud Build / Render auto-deploy on push to `main`. Failed deploys roll back to the previous live revision automatically. Manual rollback is `gcloud run services update-traffic --to-revisions=<prior-rev>=100` on Cloud Run or the equivalent Render redeploy.

## 9. Operational Controls

- **Application hardening.** Every public API runs behind Helmet (security headers), CORS allowlist, body-size limits, input validation, and per-route rate limiting. Cost-Guard middleware enforces per-tier daily and monthly call limits on AI endpoints with bonus-call accounting for paid top-ups and referrals.
- **Audit logging.** Security-relevant events are written to an `audit_event_log` table or equivalent file sink: authentication outcomes, password resets, token revocations, AI guardrail triggers (prompt injection / role override / safety bypass attempts), and admin operations. Logs are retained for at least 90 days.
- **Backups & disaster recovery.** Managed-provider point-in-time recovery covers production databases. The recovery-time objective (RTO) is 24 hours and the recovery-point objective (RPO) is 24 hours for consumer apps in the current single-founder operating posture.
- **Monitoring.** Sentry captures application errors. Render and Cloud Run dashboards surface availability. The Managing Member reviews error dashboards weekly and after every production deploy.

## 10. Privacy & Regulatory Posture

- **CCPA / GDPR right to access.** Self-serve data export available in every product that holds Confidential or Restricted data (`GET /api/auth/me/export` on Patet; equivalent endpoints to be confirmed on each launching app).
- **Right to erasure.** Account deletion (`DELETE /api/auth/me`) cascades to all per-user tables via foreign-key `ON DELETE CASCADE`. Plaid items are revoked at the Plaid API on account deletion. The data-retention default is "delete on account-close" for Confidential data and "anonymize on account-close" for aggregate analytics.
- **Children's data.** No Plainly Digital product knowingly collects data from users under 13 (COPPA). Patet's published audience is 18-28. Apps with potentially younger users (e.g., future K-12 financial-literacy curriculum licensing) will gate at the school/district account level rather than collect individual children's data.
- **Financial-advice posture.** Plainly Digital products do not provide licensed financial, legal, or medical advice. AI coach output is educational; users in financial crisis are directed to 211.org, federal student-loan hardship options, and other regulated resources. No money-movement features (transfers, sweeps, automated payments) are offered.

## 11. Training, Awareness & Review

- **Founder / employee training.** The Managing Member completes a refresher each calendar year on (a) phishing recognition, (b) secret-handling, (c) data-classification rules in §3, and (d) the incident-response flow in §7. Future employees and contractors complete the same training during their first 30 days and annually thereafter.
- **Customer awareness.** Customer-facing security guidance is published at `https://plainlydigital.com/security` and within each app's privacy policy. The `.well-known/security.txt` file lists the disclosure channel.
- **Policy review.** This document is reviewed at least annually by the Managing Member. Material changes to vendors, regulatory requirements, or product scope trigger an out-of-cycle review within 30 days. The version history is preserved in git; changes are committed with descriptive messages.

## 12. Acknowledgement

By accepting this policy, the Managing Member (and any future employee or contractor with production access) commits to:

- Following the controls in §3-§11.
- Reporting suspected incidents via the channel in §7 immediately.
- Refusing to bypass any control without written risk-acceptance from the Managing Member.

---

**Signed:** Jonathan Brock, Managing Member, Plainly Digital LLC
**Date:** 2026-05-11
