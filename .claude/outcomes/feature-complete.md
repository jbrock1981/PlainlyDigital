# Rubric: feature-complete

**When to apply:** Use to grade whether a feature branch is shippable to staging. This is a generic baseline — most features should add 2-4 feature-specific criteria on top.

**Verdict thresholds:**
- PASS: every criterion PASS
- PARTIAL: PASS/PARTIAL mix, no FAIL
- FAIL: any FAIL, or more than half PARTIAL

## Criteria

### 1. Functionality
- **Statement:** The feature does what the spec / plan said it would do.
- **How to verify:** Read the original plan, walk through each user-facing behavior, confirm by running the app or reading test cases.
- **Pass evidence example:** "Plan called for OAuth login → screen at /login completes Google sign-in, lands on /dashboard. Verified manually + via e2e test test_oauth_happy_path."
- **Fail evidence example:** "Plan called for refresh token rotation; no rotation logic in src/auth/. Test for it is missing."

### 2. Tests
- **Statement:** New or modified code paths have tests covering happy path AND at least one error/edge case.
- **How to verify:** Run the test suite. Check coverage of the new files via `git diff --stat` cross-referenced to test files.
- **Pass evidence example:** "src/auth/oauth.ts changes mirrored by tests in test/auth/oauth.test.ts; tests pass; covers success + expired token + missing scope."
- **Fail evidence example:** "src/auth/oauth.ts has no corresponding test file. Or tests exist but cover only happy path."

### 3. Error handling
- **Statement:** All external calls (network, DB, third-party APIs) handle failure explicitly. No silent catches.
- **How to verify:** Grep for try/catch, fetch, await on external APIs. Check each has a defined failure path.
- **Pass evidence example:** "All Supabase calls in src/db/ wrapped in try/catch with logged error + user-facing fallback."
- **Fail evidence example:** "fetch() in src/api/checkout.ts has no .catch and no try/catch wrapper."

### 4. Logs and observability
- **Statement:** Important state transitions and errors are logged at appropriate levels. No PII or secrets in logs.
- **How to verify:** Read added logging statements; grep for `console.log` / `console.error`. Verify no req.body, no passwords, no tokens.
- **Pass evidence example:** "Auth events logged with userId only; errors include error.message but not stack traces with secrets."
- **Fail evidence example:** "console.log(req.headers) in middleware leaks Authorization header."

### 5. Docs
- **Statement:** If the feature changes an API, env var, or user-facing behavior, the relevant doc is updated. CLAUDE.md updated if a convention changed.
- **How to verify:** Check docs/, README.md, CLAUDE.md, .env.example for references that should now exist.
- **Pass evidence example:** "Added GOOGLE_OAUTH_CLIENT_ID to .env.example and README setup section. CLAUDE.md notes auth approach."
- **Fail evidence example:** "Feature adds new env var but .env.example unchanged."

### 6. No regression
- **Statement:** Existing tests still pass. No removed functionality unless explicitly noted in the plan.
- **How to verify:** Run full test suite. Compare git diff for deletions.
- **Pass evidence example:** "Full suite green; deletions limited to dead code identified in plan."
- **Fail evidence example:** "test_billing_upgrade fails after changes; was not addressed in plan."

### 7. Type safety / lint
- **Statement:** Build passes; type-checker passes; linter passes.
- **How to verify:** Run `npm run build`, `npm run typecheck`, `npm run lint` (or repo equivalents).
- **Pass evidence example:** "All three commands exit 0."
- **Fail evidence example:** "tsc reports 3 errors in src/auth/oauth.ts."

## Notes for the grader

- If a criterion doesn't apply (e.g., a frontend-only repo with no DB calls for criterion 3), mark it PASS with a note "N/A — no external calls in this change."
- For repos without a test framework, criterion 2 grades against "manual reproduction steps documented in PR description" instead.

## Revision history

- 2026-05-06 — initial draft
