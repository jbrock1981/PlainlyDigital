# Rubric: route-compliance

**When to apply:** Any change that adds or modifies a backend route module under your project's routes directory (e.g., `api/src/routes/`, `app/api/`, `server/handlers/`). Use `/outcome route-compliance --git HEAD` to drive a route to passing.

**Why this rubric exists:** Backend routes are the surface where security, audit, and data-correctness invariants matter most. The loop of "write route → grade → fix gaps" works best as a real autonomous flow rather than a one-shot lint.

**Configure for your project:**
- Replace `<your-auth-middleware>` with the name of your auth middleware (e.g., `requireAuth`, `authenticate`, `withSession`).
- Replace `<your-rbac-helper>` with your role/capability check (e.g., `requireRole('admin')`, `requireStaff()`).
- Replace `<your-validation-lib>` with your input validator (e.g., zod, joi, yup, manual whitelist).
- Replace `<your-audit-helper>` with your audit-logging function name.
- Replace `<your-logger-import>` with your structured logger import.

**Verdict thresholds:** PASS / PARTIAL / FAIL per the standard rules.

## Criteria

### 1. Auth gate present
- **Statement:** Every non-public handler is wrapped in `<your-auth-middleware>` (or the equivalent middleware for the route's intended audience). Public endpoints must be explicitly justified in a comment AND mounted at a documented public path.
- **How to verify:** Inspect each handler. For each one without auth middleware, confirm a comment explains why and the path matches the documented public surface.
- **Pass evidence example:** "All POST/PUT/DELETE handlers wrapped in auth middleware; one GET handler is public with a `// PUBLIC: see CLAUDE.md <section> block` comment."
- **Fail evidence example:** "POST /api/foo handler has no auth middleware and is not on the documented public surface."

### 2. RBAC / role check enforced where appropriate
- **Statement:** Routes that mutate org data, billing, secrets, sensitive integrations, or staff-only resources include the appropriate role / capability check (`<your-rbac-helper>`).
- **How to verify:** Inspect each handler against the route prefix's expected audience. Admin-only routes need an admin check. Staff-only routes need a staff check.
- **Pass evidence example:** "Routes under `/api/secrets` all check `req.user.role === 'admin'` for mutations."
- **Fail evidence example:** "POST `/api/staff/provision-customer` accepts requests from any authenticated user."

### 3. Validation on inputs
- **Statement:** All request bodies / params / query strings are validated against an explicit schema (`<your-validation-lib>` or a manual whitelist) before use. UUID and pagination params are bounded.
- **How to verify:** Grep for `req.body.`, `req.params.`, `req.query.` usage in the handler. Each access should follow a validation step.
- **Pass evidence example:** "Body parsed with `FooBodySchema.parse(req.body)`; UUID param validated via `zUuid.parse(req.params.id)`."
- **Fail evidence example:** "Handler reads `req.body.amount` directly with no validation; potential type coercion / NaN bug."

### 4. Audit row written for sensitive actions
- **Statement:** Sensitive mutations (secret reveal, compliance recommendation creation, staff provisioning, integration sync, etc.) write an audit row in the same transaction as the mutation. Reads of secrets are also audit-logged.
- **How to verify:** Trace mutation paths. Confirm a `<your-audit-helper>` call exists in the same transaction as the mutation.
- **Pass evidence example:** "Reveal endpoint writes audit row inside the same `BEGIN/COMMIT` as the decrypt."
- **Fail evidence example:** "Rotate endpoint mutates the row but writes the audit log only on success and only outside the transaction — partial-failure leaves no evidence."

### 5. Structured logger, no `console.*`
- **Statement:** All logging uses `<your-logger-import>`. No `console.log`, `console.error`, `console.warn`. Errors include enough context (request id, org id, user id) to debug without exposing secrets.
- **How to verify:** Grep for `console.`. Read added logger statements for secret leakage.
- **Pass evidence example:** "All logging via the structured logger; no console.*."
- **Fail evidence example:** "`console.error(err)` in catch block — escapes structured logger and may include sensitive stack frames."

### 6. Tests exist
- **Statement:** New or modified routes have unit tests in your project's tests directory. Tests cover happy path, an unauthorized path (401 / 403), and at least one validation-failure path (422).
- **How to verify:** Confirm a corresponding test file exists. Run it with your unit-test runner.
- **Pass evidence example:** "Test file covers 200, 401, 422; tests green."
- **Fail evidence example:** "Route added without test file."

### 7. Route-compliance-checker clean (if your project has one)
- **Statement:** Your project's route-compliance-checker reports no violations for changed files.
- **How to verify:** Run the script.
- **Pass evidence example:** "Checker output: 'All routes compliant.'"
- **Fail evidence example:** "Checker flags missing audit log on `routes/foo.ts:74`."

## Notes for the grader

- Webhook routes that need raw bodies (Stripe webhooks, Git provider webhooks, etc.) are typically mounted with `express.raw` BEFORE the global JSON parser. If a new route follows that pattern, the rubric still applies but criterion 3 (validation) has different mechanics — confirm signature verification on raw bytes, then schema-validate the parsed body.
- Public routes (lead capture, status pages, attestation transparency endpoints) are exempt from criterion 1 but must still satisfy 3, 5, 6, 7.

## Revision history

- <YYYY-MM-DD> — initial draft
