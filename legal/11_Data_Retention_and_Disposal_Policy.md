# Plainly Digital LLC — Data Retention and Disposal Policy

**Document version:** 1.0
**Effective date:** 2026-05-17
**Owner:** Jonathan Brock, Managing Member (Plainly Digital LLC)
**Review cadence:** Annual (next scheduled review: 2027-05-17), or within 30 days of (a) a material change to applicable data-privacy law, (b) the addition of a new product or data category, or (c) a change in the data processors listed in §4.
**Governing law:** Tennessee, USA. Applicable consumer-privacy frameworks: GDPR (EEA/UK users), CCPA / CPRA (California users), COPPA (under-13 users — see §8), and equivalent state laws where users reside.
**Companion documents:** Information Security Policy §10 (Privacy & Regulatory Posture) and §11 (Training, Awareness & Periodic Review) provide the broader privacy posture; Access Control Policy §8.3 (Audit-log retention) and §8.4 (Periodic access review) provide the related access-side controls. This document is canonical for the *retention and disposal* of personal and operational data.

---

## 1. Purpose & Scope

This Data Retention and Disposal Policy defines, for every data category Plainly Digital LLC ("Plainly Digital," "the Company") processes, (a) how long that data is retained, (b) what triggers its deletion, (c) the method by which it is disposed of, and (d) how this policy is reviewed and kept current with applicable privacy law.

The policy implements GDPR Article 5(1)(e) (storage limitation), GDPR Article 17 (right to erasure), CCPA/CPRA §1798.105 (right to delete), and is the operational source-of-truth referenced by partner due-diligence forms (Plaid IAM review, GCP partner program, App Store / Google Play data-handling questionnaires).

**Scope.** This policy applies to every system, vendor, employee, contractor, and customer that interacts with Plainly Digital production assets, including:

- The marketing site at `https://plainlydigital.com`
- The Patet personal-finance product (consumer + future B2B curriculum licensing)
- The Vinla, Winlet, Glyphe, CastFreely, Tradingly, Fraus, Salvis, ClearDoc, SitterSheet products
- All managed-database instances (Neon Postgres, Cloud SQL, Firebase Firestore, Supabase Postgres)
- All hosting platforms (Render, Vercel, Firebase Hosting, Cloud Run)
- All third-party processors (Anthropic Claude, Plaid, RevenueCat, Resend, Sentry)

## 2. Principles

Plainly Digital follows five operating principles for data retention and disposal:

1. **Storage limitation.** Personal data is retained only for as long as it serves the purpose for which it was collected (GDPR Art. 5(1)(e)).
2. **Trigger-based deletion.** Each data category has at least one explicit deletion trigger (account close, bank disconnect, age-out timer, or user request). No data is retained indefinitely by default.
3. **Erasure on request.** Account deletion via the in-product self-serve flow erases all personal data within 30 days, subject to narrow legal-retention carve-outs called out in §3.
4. **Disposal at the database layer.** Where erasure is required, data is hard-deleted via `DELETE` (foreign-key `ON DELETE CASCADE` propagates to dependent rows). Backups are described in §5.
5. **Periodic review.** This policy is reviewed at least annually and on every material change to the legal or vendor landscape (§9).

## 3. Retention schedule by data category

The table below is exhaustive for personal and operational data Plainly Digital stores. Where two or more triggers apply, the *earliest* trigger governs disposal.

| Category | Retention period | Trigger(s) for deletion | Storage location | Disposal method |
|---|---|---|---|---|
| Account profile (email, name, hashed password, situation, primary worry, coach-persona preference, timezone, locale, role) | Lifetime of active account | Account closure via `DELETE /api/auth/me`; purge completes within 30 days. | Neon Postgres `users` table (`royal-lake-78408653`) | Hard `DELETE`, FK `ON DELETE CASCADE` removes dependent rows in 30+ child tables. |
| Lesson progress, achievements, daily-challenge completions, streak history, XP | Lifetime of active account | Account closure (30-day purge). | Neon Postgres `lesson_progress`, `streaks`, `user_xp`, `xp_events`, `user_achievements`, `user_challenge_completions` | Hard `DELETE` via CASCADE. |
| AI coach conversation messages | Rolling 30 days | Per-conversation user delete; account closure (30-day purge); automatic rolling expiry via scheduled job. | Neon Postgres `coach_messages` | Hard `DELETE` (per message) and scheduled cron-driven row purge for messages > 30 days old. |
| Financial PII at rest (monthly_take_home, monthly_fixed_expenses, current_savings, debt balances, debt minimum payments) | Lifetime of active account, AES-256-GCM encrypted via migration 017 | Account closure (30-day purge). | Neon Postgres `financial_snapshots`, `debts` (encrypted columns) | Hard `DELETE` via CASCADE. Encryption key remains owned by Plainly Digital; key is not destroyed at row delete because it is shared across all rows. |
| Plaid item access tokens | Lifetime of connected bank | User disconnects bank in app (immediate revocation + delete); account closure (30-day purge). | Neon Postgres `bank_connections` (AES-256-GCM encrypted) | Call to Plaid `itemRemove` revokes the token at Plaid; then hard `DELETE` of the local encrypted row. |
| Plaid transaction history, statement-extracted transaction history, category overrides | Lifetime of active account | Per-transaction user delete; per-upload user delete (statement uploads); bank disconnect (cascades to all transactions for that item); account closure (30-day purge). | Neon Postgres `transactions`, `statement_uploads`, `transaction_category_overrides` | Hard `DELETE` via CASCADE. **Uploaded statement files (PDF/CSV/Excel binaries) are never stored** — only the extracted transactions are persisted. |
| Subscription receipts / RevenueCat events / payment history | 7 years | IRS / state-tax record-keeping requirement. Aged-out after 7 years via scheduled job. Survives account deletion as required for tax compliance (see §3.1 — legal carve-out). | Neon Postgres `user_usage`, RevenueCat dashboard | Hard `DELETE` of the local row at the 7-year boundary. RevenueCat retention follows their published policy at https://www.revenuecat.com/privacy. |
| Audit log / security events (system_audit_log) | 24 months | Aged-out automatically via scheduled job. | Neon Postgres `system_audit_log` | Hard `DELETE` of rows with `created_at < NOW() - INTERVAL '24 months'`. |
| Authentication-event stdout logs (login attempts, token refresh, MFA, password-reset) | 90 days | Aged-out automatically by hosting platform (Render log retention defaults). Migrating to GCP Cloud Logging Q3 2026 with the same 90-day retention configured. | Render / Cloud Run stdout, structured JSON | Platform-managed rotation; no manual disposal needed. |
| Session inventory + revoked-token list | Until JWT natural expiry + 30 days | Token expiry (7 days from issuance) + a 30-day grace for forensic review; row then purged via scheduled job. | Neon Postgres `user_sessions`, `revoked_tokens` | Hard `DELETE`. |
| Password-reset tokens / email-verification tokens | 1 hour (reset) / 24 hours (verify) | Single-use consumption OR scheduled expiry — whichever is sooner. | Neon Postgres `password_reset_tokens`, `email_verify_tokens` | Hard `DELETE` of expired and consumed rows. |
| TOTP MFA secrets + recovery codes | Lifetime of active account | User disables MFA (`POST /api/auth/mfa/disable`); account closure (30-day purge). | Neon Postgres `user_mfa` (AES-256-GCM encrypted secret; sha256-HMAC recovery code hashes) | Hard `DELETE`. Recovery codes consumed in the normal challenge flow are nulled in place (single-use), not deleted. |
| Push notification tokens | Lifetime of active device registration | Token marked inactive on registration churn; account closure (30-day purge). | Neon Postgres `push_tokens` | Hard `DELETE`. |
| Anonymized crash + error data | 90 days | Aged-out automatically by Sentry. | Sentry (third-party processor) | Vendor-managed retention; see https://sentry.io/legal/privacy. |
| Aggregated, anonymized analytics (cohort benchmarks, peer comparisons, lesson-completion rates) | Indefinite | Not personally identifiable after aggregation; minimum cohort size of 20 enforced per CLAUDE.md to prevent re-identification (k-anonymity). | Neon Postgres `cohort_benchmarks`, derived views | Not subject to user-erasure right because the data is anonymized in place at write time; the user-identifying source rows are deleted on account closure. |
| Affiliate clicks / impressions (hashed user id, partner, product, timestamp) | 18 months | Aged-out automatically via scheduled job; commission reconciliation requires up to 90-day partner reporting lag, so we retain past that. | Neon Postgres `affiliate_clicks`, `affiliate_impressions` | Hard `DELETE` of rows > 18 months old. |
| Marketing-list email subscriptions (Plainly Digital marketing site) | Until unsubscribe | User unsubscribe via list-unsubscribe header or in-email link. | Resend (third-party processor) | Resend-managed delete on unsubscribe. |
| Onboarding-email drip log | 90 days | Aged-out automatically via scheduled job after the 4-email sequence is fully sent or skipped. | Neon Postgres `onboarding_email_log` | Hard `DELETE` of rows > 90 days old. |
| Gift codes + redemption records | 24 months past redemption (or expiry) | Aged-out via scheduled job after the longer of (a) 24 months past redemption or (b) gift expiry. | Neon Postgres `gift_codes` | Hard `DELETE`. |
| Patet Certified™ credential records | Lifetime (credential is intentionally durable) | Holder-initiated revocation; account closure deletes the credential record but the public verify endpoint then returns `not found`. | Neon Postgres `certifications` | Hard `DELETE` via CASCADE on account closure. |

### 3.1 Legal-retention carve-outs

The following narrow exceptions survive a user's account deletion request because applicable law requires us to retain them:

- **Tax records.** Subscription receipts and revenue records are retained for 7 years to satisfy IRS and state-tax record-keeping requirements (26 U.S.C. § 6001; Treas. Reg. § 1.6001-1). Records are retained in a form that does not surface personal contact information beyond what the tax record itself requires (transaction id, amount, date, jurisdiction).
- **Fraud / security investigations.** If a user account is deleted while it is the subject of an open fraud investigation, the audit-log rows referencing that account are retained until the investigation closes, then purged on the next quarterly review.
- **Legal hold.** If a court order, subpoena, or written preservation request from law enforcement is received, the implicated data is placed under legal hold and excluded from routine disposal until the hold is released in writing.

Outside these three exceptions, account deletion is comprehensive.

## 4. Third-party processors

Each processor below holds personal data on Plainly Digital's behalf. Plainly Digital has a Data Processing Agreement (or equivalent contractual commitment) with each, and each is contractually bound to honor an erasure request propagated by Plainly Digital.

| Processor | Data held | Retention controlled by | Erasure mechanism |
|---|---|---|---|
| Neon (Postgres) | All persistent personal + transactional data | Plainly Digital (per the schedule in §3) | `DELETE` SQL issued by application code |
| Render (API hosting) | Stdout logs only | Render platform (90-day rotation) | Automatic |
| Vercel (web hosting) | CDN access logs + edge metrics | Vercel platform (~30 days) | Automatic; Vercel dashboard self-serve where supported |
| Plaid | Bank account access tokens, transaction history mirrored from the user's bank | Plainly Digital triggers, propagated to Plaid via `itemRemove` API | Plaid removes the item server-side on `itemRemove`; users may also call Plaid directly to revoke access |
| RevenueCat | Subscription receipt + entitlement data | Plainly Digital (7-year tax retention; see §3.1) | RevenueCat dashboard delete-customer API |
| Anthropic Claude (AI coach) | Prompt + response payloads only for the duration of the API call; Anthropic does not retain training data per their zero-retention API tier | Anthropic platform | API requests are not retained beyond the 30-day operational log per Anthropic's Commercial Terms |
| Resend (transactional email) | Recipient email + email bodies for delivery + bounce tracking | Resend platform (30-day default) | Resend dashboard self-serve delete |
| Sentry (error tracking) | Stack traces + anonymized request context | Plainly Digital config (90-day retention) | Sentry self-serve project-level retention setting |
| Render Cron (onboarding-email dispatcher) | No data — runs against Neon | n/a | n/a |

## 5. Backups

Production database backups are taken automatically by Neon and retained for **7 days** on the Neon free tier (current posture). Backups are encrypted at rest by Neon. When a user requests erasure, the deletion is applied to the live database immediately; the trailing 7-day backup window will continue to contain the user's data until the backups age out, at which point the user's data is gone from all backups. This is documented to users in the Patet Privacy Policy and is consistent with GDPR EDPB Guidelines 06/2020 on the right to erasure as it applies to backups.

When Plainly Digital migrates a product to a paid Neon tier (or to Cloud SQL on GCP), this section will be re-reviewed and updated for the new backup-retention window.

## 6. Disposal mechanisms (summary)

- **Hard `DELETE` with `ON DELETE CASCADE`** is the primary disposal mechanism. All per-user tables have FK constraints back to `users(id)` with `ON DELETE CASCADE`, so a single `DELETE FROM users WHERE id = $1` propagates to every dependent row in one transaction.
- **Application-layer encryption** (AES-256-GCM, key in `ENCRYPTION_KEY` env var) is applied to Plaid access tokens and financial PII (migration 017). The encryption key itself is rotated annually (next rotation: 2027-05-09) following the procedure in InfoSec Policy §7. After deletion, even a database backup containing the deleted row's ciphertext is unreadable without the key.
- **Anonymization** is used for analytics: cohort benchmarks, peer comparisons, and lesson-completion rates are aggregated at write time with a minimum cohort size of 20, so individual users cannot be re-identified from the aggregate. The user-identifying source rows are still deleted on account closure.
- **Scheduled jobs** purge rows that age out: a Render cron (`patet-data-retention`) runs nightly to delete rows older than the retention boundary in §3 for `coach_messages`, `affiliate_clicks`, `affiliate_impressions`, `system_audit_log`, `onboarding_email_log`, and expired tokens.

## 7. User rights and self-service

- **Right to access.** Users may export a full data bundle via `GET /api/auth/me/export` (authenticated, attachment response). The export omits internal admin tables and active password-reset/email-verify tokens; everything else is included.
- **Right to deletion.** Users may delete their account via `DELETE /api/auth/me` (authenticated) or by emailing `support@plainlydigital.com`. Deletion is effective immediately on the live database; backups age out within 7 days (§5).
- **Right to correct.** Users may correct their name, situation, and primary worry in the Patet profile screen (PATCH `/api/auth/me`).
- **Right to disconnect a bank.** Users may disconnect Plaid in the Patet profile screen at any time; the access token is revoked at Plaid (`itemRemove`) and locally deleted in one operation.
- **Right to portability.** The data export at `GET /api/auth/me/export` is delivered as JSON and is machine-readable per GDPR Art. 20.
- **Children's data (under 13).** Plainly Digital does not knowingly collect data from users under 13 (COPPA). If a parent or guardian believes a child has registered, they may email `support@plainlydigital.com` and the account will be deleted within 5 business days regardless of the standard 30-day purge window.

## 8. Vendor incident response

If a third-party processor listed in §4 notifies Plainly Digital of a data-handling incident affecting our data, Plainly Digital follows the incident-response procedure in InfoSec Policy §8, including (a) confirming whether personal data was affected, (b) notifying affected users within 72 hours if required by GDPR Art. 33 or applicable state law, and (c) re-evaluating the processor's continued use.

## 9. Periodic review

This policy is reviewed:

- **Annually**, on or before the effective-date anniversary, by the Managing Member. The review checks for changes in applicable privacy law, addition/removal of processors, and accuracy of the §3 schedule against actual database state.
- **Within 30 days of any material change** to: applicable data-privacy law (e.g., a new state law that creates retention requirements), the addition of a new product or data category, a change in any of the third-party processors in §4, or a finding from a security audit or penetration test.
- **Within 24 hours of an incident** that exposes a flaw in the disposal mechanism (e.g., a CASCADE missing on a new table). The review documents the root cause and the fix.

The most recent review is recorded in the revision history (§10).

## 10. Revision history

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-05-17 | Jonathan Brock | Initial version. Consolidates retention/disposal content previously scattered between Information Security Policy §10/§11, Patet Privacy Policy §4, and Plaid IAM evidence packet. Created to satisfy Plaid Q11 ("Provide your Data Retention and Disposal Policy"). |
