# Plainly Digital LLC — Access Control Policy

**Document version:** 1.0
**Effective date:** 2026-05-11
**Owner:** Jonathan Brock, Managing Member (Plainly Digital LLC)
**Review cadence:** Annual (next scheduled review: 2027-05-11), or within 30 days of any material change to roles, vendors, or applicable law.
**Governing law:** Tennessee, USA.
**Companion documents:** Information Security Policy (§4 of Document 04 summarizes; this document is canonical for access-control controls).

---

## 1. Purpose & Scope

This Access Control Policy defines how Plainly Digital LLC ("Plainly Digital," "the Company") limits, authorizes, monitors, and reviews access to production assets and sensitive data. It implements the access-control controls referenced in the Information Security Policy §4 in detail sufficient for partner due diligence (Plaid, GCP, App Store Review, Google Play, future SOC 2 readiness).

Where a control listed below maps to a NIST SP 800-53 Rev 5 AC- or IA-family identifier, that identifier is shown in brackets for reference. Plainly Digital is not formally FedRAMP-authorized; the mapping is for clarity and audit traceability, not a claim of certification.

**Scope.** This policy applies to every system, vendor, employee, contractor, and customer that interacts with Plainly Digital production assets, including but not limited to:

- The marketing site at `https://plainlydigital.com`
- The Patet personal-finance product (consumer + future B2B curriculum licensing)
- The Vinla, Winlet, Glyphe, CastFreely, Tradingly, Fraus, Salvis, ClearDoc, SitterSheet products
- All managed-database instances (Neon Postgres, Cloud SQL, Firebase Firestore, Supabase Postgres)
- All hosting platforms (Render, Vercel, Firebase Hosting, Cloud Run)
- All AI-vendor integrations (Anthropic Claude, Plaid, RevenueCat, Resend)

## 2. Roles & Responsibilities

| Role | Held by | Access scope | Authorization owner |
|---|---|---|---|
| Managing Member / Security Officer | Jonathan Brock | All production assets, all vendors, all customer data. | Self (signed acknowledgement in §10). |
| Engineering | Jonathan Brock (solo founder) | All production assets via Managing Member identity. | Managing Member. |
| Future Employees / Contractors | None as of 2026-05-11 | Scope-limited per role; default is least-privilege. | Managing Member with written role definition. |
| Customers (App Users) | App users | Their own account data and lawful use of product features. | Self-service via the product. |
| Cron / Automation | Render scheduled jobs, GCP Cloud Scheduler | Server-to-server identity via `INTERNAL_API_KEY` or service-account JWT; no human credentials. | Managing Member configuration. |
| Periodic Reviewer | Managing Member (today); future Security Officer (when hired) | Read-only access to `system_audit_log` and active-session inventory. | Managing Member. |

Because Plainly Digital is a solo-founder LLC, the Managing Member fulfills the "system owner," "data owner," and "access approver" roles defined in NIST SP 800-53 [AC-1]. Any future hire whose role touches production or customer data inherits the responsibilities in this policy on their first day and acknowledges it in writing.

## 3. Account Management [AC-2]

### 3.1 Account types

Plainly Digital recognizes the following account types and assigns each a documented privilege baseline:

| Account type | Examples | Privilege baseline | De-provisioning trigger |
|---|---|---|---|
| **Customer / consumer** | App user with email-password or OAuth credential. | Own account data only. Subject to tier-based feature gates (Free / Pro / Pro+). | Self-serve `DELETE /api/auth/me` or 30-day inactivity for ToS-violating accounts after notice. |
| **Operator / Support** | Future Plainly Digital support staff. | `role='support'` — read-only across audit log, customer metadata, billing status. **Cannot** mutate accounts, run maintenance jobs, or grant roles. | Managing Member action within 24 hours of off-boarding. |
| **Administrator** | Managing Member; future Security Officer. | `role='admin'` — full read + mutate including maintenance jobs, role grants, audit-log reads, ROAS data, content moderation. | Managing Member action within 4 hours of off-boarding. |
| **System / Service** | Render cron `INTERNAL_API_KEY`, Plaid webhook signing key, RevenueCat webhook signing key, GCP service account JWT. | Single-purpose per credential. Cron keys can dispatch onboarding emails but not query customer data outside the dispatch endpoint. | Rotation on suspected exposure (§7); planned rotation per §5. |

The role taxonomy is enforced at the database level by the `users.role` column (CHECK constraint `IN ('user', 'support', 'admin')`, migration 022) and at the application layer by the `requireRole(...allowed: Role[])` middleware in `server/src/lib/rbac.ts` of each affected product. A user without a role assignment defaults to `'user'` (consumer) — the principle is fail-closed: no implicit privilege escalation.

### 3.2 Account lifecycle

- **Creation.** Customer accounts are created by self-serve registration with email verification. Operator and Administrator accounts are created by the Managing Member running a documented role-grant via `POST /api/admin/roles` (audit-logged) after written role assignment.
- **Modification.** Privilege changes are written via the same audited `POST /api/admin/roles` endpoint. Every grant or revoke produces a `system_audit_log` row with actor, target, prior role, and new role.
- **Periodic review.** The Managing Member reviews the active operator/administrator inventory at least quarterly (next scheduled review: 2026-08-11) and the active customer-session inventory monthly for anomalies (concurrent sessions from disparate regions, unexpected user-agent strings).
- **De-provisioning.** Off-boarding revokes all access tokens held by the departing party within 24 hours (4 hours for Administrator-tier). The Managing Member maintains an access-ownership inventory in the engineering ops journal. **Automated de-provisioning (e.g., HRIS-triggered SCIM)** is not yet implemented — appropriate to the company's current single-founder posture; will be revisited at headcount ≥3.

## 4. Identity & Authentication [IA-2, IA-5, IA-8]

### 4.1 Customer authentication

- **Primary factors.** Email + password (bcrypt-hashed with cost factor ≥10) **or** Google OAuth 2.0 **or** Apple Sign-In. Apple identity tokens are verified against the Apple JWKS endpoint on every login.
- **Password requirements.** Minimum 8 characters; rejects the 10,000 most common breached passwords from the haveibeenpwned k-anonymity API at registration and reset time.
- **Account lockout** [AC-7]. Persistent failed-attempt counters live in an `account_lockout` Postgres table. Threshold: 10 failed attempts in 15 minutes → 15-minute cooldown. Counters survive Render process restarts (closes audit defer-item M11).
- **Timing equalization.** Login response time is equalized across the "email does not exist" and "wrong password" branches via a precomputed dummy bcrypt hash so attackers cannot enumerate registered emails by side-channel.
- **Multi-factor authentication (MFA).** On the active roadmap (audit defer-item L10). MFA will be **required** before connecting a Plaid bank account on any consumer product that integrates Plaid. The phased rollout is: (a) TOTP MFA available as opt-in for all users (target Q3 2026); (b) MFA mandatory for accounts with a connected Plaid item (target before commercial Patet launch); (c) MFA mandatory for any account with `role='admin'` or `role='support'` (already enforced today via the operational reality that there is exactly one such account, behind the Managing Member's hardware-key-protected primary identity).

### 4.2 Operator / Administrator authentication

- **Identity binding.** Operator and Administrator privileges attach to a normal customer JWT identity that has been promoted via `POST /api/admin/roles`. There is no shared "root" admin account.
- **Hardware-key second factor.** The Managing Member's identity (Google account + GCP, GitHub, Render, Vercel, Neon, Apple Developer, RevenueCat, App Store Connect, Play Console) requires a hardware security key (FIDO2/WebAuthn) as the second factor. Recovery codes are stored in a sealed offline backup.
- **Periodic credential rotation.** Hardware key rotation: annual unless lost or compromised. OAuth refresh tokens for vendor consoles: re-issued automatically on the vendor's TTL.
- **Internal API key.** The `INTERNAL_API_KEY` shared secret for cron access is a 32-byte random value; rotated at least annually (last rotation: 2026-05-09) and immediately on suspected exposure.

### 4.3 Service-to-service authentication

- **Plaid webhooks.** Verified by signature against Plaid's signing key on every receipt (`POST /api/plaid/webhook` rejects unsigned or wrong-signed bodies).
- **RevenueCat webhooks.** Verified against `REVENUECAT_WEBHOOK_AUTH` constant-time shared secret.
- **Affiliate-partner webhooks.** Per-partner adapters (Self, SoFi, Marcus, YNAB, Fidelity) verify signature, idempotency key, or shared-secret as documented per partner. Unverified posts return `401`.
- **Cron.** Render cron jobs and (future) Cloud Scheduler jobs authenticate to the API tier via the `x-internal-api-key` header; the receiving handler does a constant-time compare against `process.env.INTERNAL_API_KEY` before any side effect.

## 5. Access Enforcement [AC-3]

### 5.1 Access enforcement at the application layer

- **JWT-based session identity.** Every authenticated request carries a signed JWT (HS256, 256-bit secret) bound to a random `jti` (JWT ID). The middleware `requireAuth` verifies the signature, verifies the user still exists, and rejects any token whose `jti` is on the persistent `revoked_tokens` list (migration 016).
- **Role-based authorization.** The middleware `requireRole(...allowed: Role[])` enforces role membership against the database-stored `users.role` column. The role check is cache-coherent for 30 seconds; role revocation flushes the cache atomically via `invalidateRoleCache(userId)`.
- **Internal-key bypass for cron.** `requireRole` recognizes a valid `INTERNAL_API_KEY` as an internal-actor identity for cron paths and stamps `req.actor = { type: 'internal_key', role: 'admin' }` so audit-log rows attribute the action to the cron actor rather than dropping the actor entirely.
- **Tier-based feature gates.** Customer-tier limits (Free / Pro / Pro+) are enforced server-side by the Cost-Guard middleware on AI endpoints with per-user daily and monthly call counters; client-side tier checks are advisory only.

### 5.2 Access enforcement at the database layer

- **Row-level scoping.** Every per-user table includes a `user_id` foreign key. Application queries scope by `user_id = $1` derived from the request's JWT identity. The Managing Member periodically greps for "anti-patterns" (queries that select user rows by an attacker-controlled identifier without a `user_id` constraint).
- **Connection-string identity.** Production database connection strings use a single application role per product with `INSERT / UPDATE / SELECT / DELETE` on application tables and **no** `DROP / TRUNCATE / GRANT` privileges. DDL is performed via the migration runner under a separate elevated role.
- **PgBouncer / pooler scoping.** Where Neon's pooled connection is used, the pool size is bounded per product so a runaway thread cannot exhaust the production-side limit and starve other apps under the same Neon org.
- **Plaid access tokens.** Stored encrypted at rest with AES-256-GCM. The decryption key is held in the Render / Cloud Run environment, never written to git. Tokens are read into memory only at the moment of a Plaid API call and never logged.

### 5.3 Access enforcement at the infrastructure layer

- **GCP IAM.** Each Plainly Digital app's GCP project (`plainlydigital-www`, future per-app projects) follows a least-privilege IAM baseline. The Managing Member identity holds `Owner` on the org but day-to-day operations use lower-privileged roles (`Cloud Run Admin`, `Cloud Build Editor`, `Firebase Hosting Admin`) attached to the deploy automation rather than the human identity.
- **Render env-var scoping.** Render service env vars are scoped to a single service. Cross-service secret sharing is explicit and audited via a documented entry in the engineering ops journal.
- **Vercel project isolation.** Each Vercel project deploys to its own preview-and-production environment with project-scoped env vars.

## 6. Least Privilege [AC-6]

- **Engineering identity ≠ Owner identity.** Day-to-day commits, deploys, and customer-data investigation happen under the Managing Member's engineering identity. Owner-tier IAM and billing operations require a deliberate console-level switch — the principle is "default to the lower role; elevate only with intent."
- **Admin endpoints minimize their surface.** The `/api/admin/*` routes expose a deliberately narrow API surface: `prune`, `stats`, `affiliate/roas`, `audit` (read), `roles` (grant/revoke), `emails/dispatch` (cron-only). There is no general-purpose "execute SQL" endpoint. Maintenance scripts that need raw SQL run from the engineer's terminal against a separately-scoped role.
- **Support role boundary.** `role='support'` is read-only by design. The `/api/admin/roles` mutation endpoint is gated to `role='admin'` so a compromised support account cannot escalate.
- **Tokens are short-scoped.** Customer JWTs expire in 7 days; password-reset tokens expire in 1 hour; email-verify tokens expire in 24 hours. There is no "remember me forever" credential.

## 7. Session Management [AC-12]

Per-session metadata is recorded for every issued JWT (migration 022, `user_sessions` table) including:

- `jti` (primary key, matches the JWT's `jti` claim),
- `user_id` (foreign key with `ON DELETE CASCADE`),
- `issued_at`, `expires_at`, `last_seen_at` (lazy-updated),
- `ip` (the request's `req.ip` after `trust proxy=1`),
- `user_agent`,
- `client` (`'web' | 'ios' | 'android' | 'unknown'`),
- `revoked_at` (null while active).

### 7.1 User-visible session controls

- **List active sessions.** `GET /api/auth/me/sessions` returns the user's active sessions with the above metadata and tags the requesting session's `jti` so the UI can render "this device."
- **Revoke a specific session.** `POST /api/auth/sessions/:jti/revoke` performs an atomic, race-safe revocation: the SQL `UPDATE user_sessions SET revoked_at = NOW() WHERE jti = $1 AND revoked_at IS NULL` writes the session-side revocation, and the same handler writes the `jti` to the existing `revoked_tokens` enforcement list so the auth middleware blocks any reuse on the next request. Race losers receive `409 already_revoked`.
- **Logout.** `POST /api/auth/logout` revokes the current session and clears the `patet_session` httpOnly cookie when present.
- **Refresh.** `POST /api/auth/refresh` revokes the old token before issuing a replacement so a refresh-then-replay attacker cannot keep using the stolen token.

### 7.2 Web-session hardening

Web clients (sending `X-Patet-Client: web`) receive an httpOnly + `SameSite=Strict` + `Secure` cookie scoped to `path=/api`. The token is omitted from the JSON body. This closes the XSS-stealable surface that `localStorage` would expose (audit defer-item H1).

### 7.3 Session-termination invariants

- **Forced sign-out on password change.** All active sessions for the user are revoked when the user changes password.
- **Forced sign-out on account deletion.** `DELETE /api/auth/me` cascades to `user_sessions` via `ON DELETE CASCADE` and writes outstanding `jti` values to `revoked_tokens`.
- **Idle session expiry.** The JWT 7-day expiry is the hard ceiling. There is currently no shorter idle-timeout (`AC-11/AC-12` enhancement) for customer sessions; operator-tier sessions inherit the same 7-day TTL but use the same logout/revoke surface above plus the hardware-key second factor on the underlying vendor consoles.

## 8. Audit Logging & Periodic Review [AC-2(4), AU-2, AU-6]

### 8.1 Audit-log schema

Migration 022 introduces `system_audit_log` with the following columns:

| Column | Type | Purpose |
|---|---|---|
| `id` | `BIGSERIAL PRIMARY KEY` | Monotonic row id. |
| `actor_user_id` | `UUID REFERENCES users(id) ON DELETE SET NULL` | The user who took the action. SET NULL on user delete to preserve the audit trail post-offboarding. |
| `actor_role` | `TEXT NOT NULL` | The role attached to the actor at the time of the action (`'user' / 'support' / 'admin' / 'internal_key' / 'unknown'`). |
| `action` | `TEXT NOT NULL` | The action verb (`'admin.role_change'`, `'admin.prune_coach_messages'`, `'admin.read_audit_log'`, `'admin.read_db_stats'`, `'admin.read_affiliate_roas'`, …). |
| `target_table` | `TEXT` | Optional — the table whose rows were affected. |
| `target_id` | `TEXT` | Optional — the row id whose state changed. |
| `metadata` | `JSONB NOT NULL DEFAULT '{}'::jsonb` | Structured action context (`from`, `to`, counts, filters). |
| `ip`, `user_agent` | `INET`, `TEXT` | Source binding for the action. |
| `occurred_at` | `TIMESTAMPTZ NOT NULL DEFAULT NOW()` | Action timestamp. |

Indexes: `(actor_user_id, occurred_at DESC)`, `(action, occurred_at DESC)`, `(target_table, target_id)` — supports the three review queries below in constant time at the current data volume.

### 8.2 What is logged

Every administrator and operator action goes through `recordAudit()` in `server/src/lib/rbac.ts`. At minimum:

- Role grants and revokes.
- Coach-message pruning maintenance.
- Database-stats reads.
- Affiliate ROAS dashboard reads.
- Audit-log reads (recursive logging — the act of reading the audit log is itself audited).

Authentication outcomes (login, logout, password reset, email verification, session revoke, token refresh) are logged to the structured stdout log stream (`logAuth()` in `server/src/routes/auth.ts`) and forwarded by Render / Cloud Run into the platform's hosted log retention.

### 8.3 Audit-log retention & immutability

- **Retention.** `system_audit_log` rows are retained for **24 months** at minimum. Authentication stdout logs are retained for **90 days** by the hosting platform (Render's default) and exported to GCP Cloud Logging with a 24-month retention policy on a planned 2026-Q3 migration.
- **Best-effort writes.** `recordAudit()` catches its own errors and writes a fallback structured log entry so a database failure cannot block a user action. This is a deliberate trade-off: availability over absolute completeness. The fallback entry contains enough context (action, actor, timestamp, error) to reconstruct the missing row.
- **Append-only.** The application role used by the API tier has `INSERT` and `SELECT` on `system_audit_log` but no `UPDATE` or `DELETE`. Migration-runner role can `TRUNCATE` only as part of a fully documented backup-and-restore cycle.

### 8.4 Periodic access review

The Managing Member performs the following reviews on a documented cadence:

| Review | Cadence | Query |
|---|---|---|
| **Operator/Administrator inventory.** | Quarterly. | `SELECT id, email, role FROM users WHERE role IN ('admin','support');` Confirm every row is still authorized; revoke any stale assignment via `POST /api/admin/roles`. |
| **Recent admin actions.** | Quarterly. | `GET /api/admin/audit?since=<90-day-window>` — review every row; confirm the action was authorized and the actor was who they should have been. |
| **Concurrent-session anomalies.** | Monthly. | `SELECT user_id, COUNT(*) FROM user_sessions WHERE revoked_at IS NULL GROUP BY user_id HAVING COUNT(*) > 5;` — review users with unusually many active sessions and contact the customer if a compromise pattern is suspected. |
| **Vendor-access inventory.** | Annually. | Manual review of the access-ownership journal: every external vendor with production access (Render, Vercel, Firebase, GCP, Neon, Plaid, RevenueCat, Apple Developer, Google Play, GoDaddy/Cloud DNS) is confirmed current, and the Managing Member's contact identity at each vendor is verified. |

Each review is documented in the engineering ops journal with date, scope, and outcome. The next quarterly review is scheduled for **2026-08-11**.

## 9. Network & Remote Access [AC-17, AC-20]

- **All traffic is encrypted in transit.** TLS 1.2 minimum (TLS 1.3 preferred) for every public endpoint. The marketing site and app APIs publish HSTS with `max-age=31536000; includeSubDomains; preload`.
- **No production VPN.** The Company does not operate a private VPN; production access is via the public API tier with the controls in §5, or via vendor consoles (Render, GCP, Vercel, Neon) behind the Managing Member's hardware-key second factor.
- **Bastion.** Direct database access for incident response uses the vendor-managed bastion (e.g., Neon's SQL Editor under the Managing Member identity); ad-hoc connection strings are short-lived and rotated after the session.
- **External information systems** [AC-20]. Personal devices used by the Managing Member to access production are subject to: (a) full-disk encryption (`bitlocker` / `FileVault`), (b) screen-lock auto-engagement ≤5 minutes, (c) automatic security-update install, (d) hardware-key requirement at every admin login.

## 10. Acknowledgement

By accepting this policy, the Managing Member (and any future employee or contractor with production access) commits to:

- Following the controls in §3-§9.
- Reporting suspected misuse of any access credential to the Managing Member immediately (the Managing Member, if the credential is theirs, treats the report as a Level-0/1 incident under the Information Security Policy §7).
- Refusing to bypass any control without written risk-acceptance from the Managing Member.

---

## Appendix A — Control inheritance table

For partners and auditors, the table below maps each Plainly Digital control to the corresponding NIST SP 800-53 Rev 5 identifier and the implementation file or system. This is provided for reference; Plainly Digital has not been formally assessed against FedRAMP or any specific baseline.

| Control area | NIST identifier(s) | Implementation |
|---|---|---|
| Policy & procedures | AC-1 | This document; reviewed annually. |
| Account management | AC-2 | `users.role` column (migration 022), `requireRole()` middleware, `POST /api/admin/roles` (audited). |
| Access enforcement | AC-3 | `requireAuth` → `requireRole` chain, per-user row scoping. |
| Separation of duties | AC-5 | `role='support'` (read-only) vs `role='admin'` (read+mutate). |
| Least privilege | AC-6 | Connection-string role privileges; admin endpoint surface area. |
| Unsuccessful logon attempts | AC-7 | `account_lockout` table (Patet migration 015). |
| System use notification | AC-8 | Privacy Policy + ToS gated at registration. |
| Session lock | AC-11 | Device-level (OS / browser); not implemented at app layer. |
| Session termination | AC-12 | `revoked_tokens` (migration 016) + `user_sessions.revoked_at` (migration 022); logout + revoke endpoints. |
| Permitted actions w/o auth | AC-14 | Explicit allow-list: marketing site pages, `/api/health`, `/api/certification/verify/:id`, public Financial IQ flow, Plaid webhooks (signed), RevenueCat webhooks (signed). |
| Remote access | AC-17 | TLS-only; hardware-key MFA on vendor consoles. |
| Mobile devices | AC-19 | Personal-device baseline in §9. |
| External systems | AC-20 | Vendor inventory in IS Policy §6. |
| Information sharing | AC-21 | Per-vendor DPA + scope; documented in IS Policy §6. |
| Publicly accessible content | AC-22 | Marketing site editorial review; cookieless analytics. |
| Identification & authentication | IA-2, IA-8 | Email-pw + OAuth + Apple Sign-In; JWT identity. |
| Authenticator management | IA-5 | Password rules in §4.1; hardware-key requirement in §4.2. |
| Audit events | AU-2 | `system_audit_log` + `logAuth()` stdout stream. |
| Audit review, analysis, reporting | AU-6 | Quarterly review in §8.4. |
| Audit record retention | AU-11 | 24-month retention in §8.3. |

---

**Signed:** Jonathan Brock, Managing Member, Plainly Digital LLC
**Date:** 2026-05-11
