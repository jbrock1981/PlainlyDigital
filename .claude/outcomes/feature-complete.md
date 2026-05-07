# Rubric: feature-complete

**When to apply:** Generic baseline — use to grade whether a feature is shippable. Most features should add 2-4 feature-specific criteria on top of this.

**Verdict thresholds:**
- PASS: every criterion PASS
- PARTIAL: PASS/PARTIAL mix, no FAIL
- FAIL: any FAIL, or more than half PARTIAL

## Criteria

### 1. Functionality
- **Statement:** The feature does what the spec / plan said it would do.
- **How to verify:** Read the original plan or task description. Walk through each user-facing behavior. Confirm by running the app or reading test cases.
- **Pass evidence example:** "Plan called for adding `/api/foo`; route exists, returns expected shape, smoke test asserts 200."
- **Fail evidence example:** "Plan called for refresh-token rotation; no rotation logic in `src/auth/`. Test missing."

### 2. Tests
- **Statement:** New or modified code paths have tests covering happy path AND at least one error/edge case. Conventions to honor: new page → smoke test, new form → interaction test, new route → unit test, bug fix → regression test.
- **How to verify:** Run the project's test suite (`<your unit-test runner>`, `<your e2e runner>`). Cross-reference `git diff --stat` against test files.
- **Pass evidence example:** "Route `src/routes/foo.ts` mirrored by tests in `src/routes/__tests__/foo.test.ts`; covers 200, 401, 422 paths; tests green."
- **Fail evidence example:** "New route has no test file. Or tests exist but cover only happy path."

### 3. Type-checks pass
- **Statement:** Both backend and frontend (if applicable) type-check clean.
- **How to verify:** Run your project's type-check commands.
- **Pass evidence example:** "Both type-check commands exit 0."
- **Fail evidence example:** "Type-checker reports 3 errors in `src/routes/foo.ts`."

### 4. Logger and observability
- **Statement:** Important state transitions and errors use the project's structured logger. No `console.log` (or `print`) in production paths. No PII or secrets in logs.
- **How to verify:** Grep diff for `console.log`, `console.error`, raw `print` calls. Read added logging statements for secret/PII leakage.
- **Pass evidence example:** "All logging via the project logger; no req.body or auth headers in messages."
- **Fail evidence example:** "`console.log(req.headers)` in middleware leaks Authorization header."

### 5. Pre-commit checks clean
- **Statement:** Project pre-commit suite passes (lints, formatters, custom enforcers).
- **How to verify:** Run `<your pre-commit composite command>`.
- **Pass evidence example:** "All pre-commit checks return clean."
- **Fail evidence example:** "Linter flags 2 violations in changed files."

### 6. CLAUDE.md / docs updated if conventions or systems changed
- **Statement:** If this change adds an env var, a new architectural block, a deployment-mode gate, or a new convention, CLAUDE.md and any relevant docs are updated. New routes / migrations don't require CLAUDE.md updates by themselves.
- **How to verify:** Inspect diff. If a new env var was added, confirm `.env.example` and CLAUDE.md reflect it. If a deployment gate was introduced, confirm CLAUDE.md documents it.
- **Pass evidence example:** "Added env var `<VAR_NAME>`; documented in CLAUDE.md and `docs/deployment/ENVIRONMENT.md`."
- **Fail evidence example:** "Added a new top-level system but no architectural block in CLAUDE.md."

### 7. No regression
- **Statement:** Existing tests still pass. No removed functionality unless explicitly noted in the plan.
- **How to verify:** Run full test suite. Compare git diff for deletions.
- **Pass evidence example:** "Full test suite green; deletions limited to dead code."
- **Fail evidence example:** "`tests/billing.test.ts` fails after changes; not addressed in plan."

## Notes for the grader

- If a criterion doesn't apply (e.g., a docs-only PR has nothing to type-check), mark it PASS with a note like "N/A — docs-only change."
- For repos without a test framework (rare), criterion 2 grades against documented manual reproduction steps in the PR description.

## Revision history

- <YYYY-MM-DD> — initial draft
