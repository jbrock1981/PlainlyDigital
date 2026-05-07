# Rubric: pre-commit-clean

**When to apply:** Composite rubric — runs the full project pre-commit suite as a single grading pass. Cheap to invoke; useful as a final gate before `git commit` on any non-trivial change. `/outcome pre-commit-clean --from-recent` is the typical invocation.

**Why this rubric exists:** Most projects have several enforcement scripts (vendor-scrubber, dark-theme-enforcer, migration-validator, route-compliance-checker, security-review, lint, format). Each may have its own focused rubric. This rubric runs all of them at once for a "is this change ready to commit?" check.

**Configure for your project:** Edit each criterion below to point at your project's actual command. Drop criteria you don't have; add the ones you do.

**Verdict thresholds:** PASS / PARTIAL / FAIL per the standard rules.

## Criteria

### 1. Vendor-scrubber clean (if applicable)
- **Statement:** Your project's vendor-scrubber returns no violations.
- **How to verify:** Run the command (e.g., `<your vendor-scrubber>`).
- **Pass evidence example:** "Vendor-scrubber: no violations."
- **Fail evidence example:** "Vendor-scrubber flags 1 violation in `<frontend-src>/dashboard/foo/page.tsx`."

### 2. Dark-theme enforcer clean (if applicable)
- **Statement:** Your project's dark-theme enforcer returns no violations.
- **How to verify:** Run the command.
- **Pass evidence example:** "Dark-theme enforcer: no violations."
- **Fail evidence example:** "Enforcer flags `text-gray-900` in two changed files."

### 3. Migration validator clean (if applicable)
- **Statement:** Your project's migration validator returns no errors. (No-op if no migrations changed.)
- **How to verify:** Run the command.
- **Pass evidence example:** "Migration validator: no migrations changed, OR all valid."
- **Fail evidence example:** "Validator flags missing `IF NOT EXISTS` in new migration."

### 4. Route compliance clean (if applicable)
- **Statement:** Your project's route-compliance checker reports no violations. (No-op if no routes changed.)
- **How to verify:** Run the command.
- **Pass evidence example:** "Route compliance: no routes changed, OR all routes compliant."
- **Fail evidence example:** "Checker flags missing audit log on a new mutation route."

### 5. Security review clean (if applicable)
- **Statement:** Your project's security-review script returns no findings. Note: in many projects, security-review is non-blocking warnings — but this rubric treats them as gating because the user invoked the rubric explicitly.
- **How to verify:** Run the command.
- **Pass evidence example:** "Security review: no findings."
- **Fail evidence example:** "Security review flags `console.log` of a token in error path."

### 6. Type-checks pass
- **Statement:** Both backend and frontend (if applicable) type-check clean. This isn't a pre-commit script per se but ranks alongside them as a gate.
- **How to verify:** Run your project's type-check commands.
- **Pass evidence example:** "Both type-check commands exit 0."
- **Fail evidence example:** "Type-checker reports 1 error in changed file."

## Notes for the grader

- If your project's default pre-commit run treats some checks as non-blocking warnings (e.g., security-review), this rubric upgrades them to gating because the user explicitly invoked the rubric — that's a higher bar than the default pre-commit run.
- Run all checks in parallel where possible (they're independent).
- For an `/outcome` loop using this rubric, each iteration's fix prompt should narrow to the single failing check; don't bundle.

## Revision history

- <YYYY-MM-DD> — initial draft
