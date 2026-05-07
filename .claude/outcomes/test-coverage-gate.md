# Rubric: test-coverage-gate

**When to apply:** Any change touching your project's source directories (e.g., `api/src/**/*.ts`, `src/**/*.py`). Enforces that changed files meet a minimum line-coverage floor — most pre-commit suites don't gate on coverage, so this rubric closes that gap.

**Why this rubric exists:** Untested code is technical debt-in-flight. Without a coverage gate, a route or service can be added with zero tests and the pre-commit suite says "clean." This rubric makes coverage on changed files a first-class outcome — pair it with `feature-complete` for any route/service work and it auto-blocks merges that drop the coverage floor.

**Configure for your project:**
- Set the coverage thresholds in the table below to match your project's standards. Document them in your project's code-standards doc (`<code-standards-doc>`, e.g., `docs/CODE-STANDARDS.md`).
- `<your-coverage-runner>` — the command that runs tests with coverage (e.g., `npx vitest run --coverage`, `pytest --cov=...`, `go test -coverprofile`).
- `<your-coverage-summary-path>` — where the coverage report writes JSON output.

**Verdict thresholds:** PASS / PARTIAL / FAIL per the standard rules.

## Coverage thresholds (from `<code-standards-doc>`)

Customize this table per project. Example values:

| File category | Floor (FAIL below this) | Target (PASS above this) |
|---|---|---|
| `<your-routes-glob>` (e.g., `api/src/routes/**/*.ts`) | 35% line | 60% line |
| `<your-services-glob>` (e.g., `api/src/services/**/*.ts`) | 30% line | 50% line |
| Migration files | n/a (data) | n/a |
| Everything else under `<your-source-glob>` | 25% line | 50% line |

The "PARTIAL" band is between floor and target.

## Criteria

### 1. All changed files in `<your-source-glob>` meet the line-coverage floor
- **Statement:** For every source file that the diff modifies (added or edited — not deleted), the post-test line coverage is at least the floor for its category.
- **How to verify:**
  ```bash
  <your-coverage-runner>
  # Then read the coverage summary at <your-coverage-summary-path>
  ```
  For each changed file, look up its line-coverage % in the summary and compare against the table above.
- **Pass evidence example:** "All 4 changed files meet target: `routes/foo.ts` 71%, `services/bar.ts` 58%, `services/baz.ts` 62%, `lib/qux.ts` 54%."
- **Fail evidence example:** "`api/src/routes/auth/webauthn.ts` is at 18% — below the 35% routes floor. `api/src/services/foo/sync.ts` is at 22% — below the 30% services floor."

### 2. New files have AT LEAST one test file
- **Statement:** Any newly created source file (excluding type-only `.d.ts`, fixtures, generated files) has a corresponding test file. Naming convention: `<your-source-glob>/foo.ts` → `<your-test-glob>/foo.test.ts` (or your project's convention).
- **How to verify:**
  ```bash
  NEW=$(git diff --diff-filter=A --name-only main..HEAD -- '<your-source-glob>' | grep -v '\.d\.ts$' | grep -v 'fixtures/' | grep -v '__generated__')
  for FILE in $NEW; do
    BASE=$(basename "$FILE" .ts)
    if ! find <your-test-roots> -name "${BASE}.test.ts" -o -name "${BASE}.spec.ts" 2>/dev/null | head -1 | grep -q .; then
      echo "FAIL: $FILE has no companion test file"
    fi
  done
  ```
- **Pass evidence example:** "All 3 new files have test companions."
- **Fail evidence example:** "`<your-source-glob>/services/new-thing.ts` has no companion test file anywhere under your test roots."

### 3. Coverage hasn't regressed on neighboring files
- **Statement:** No file currently in the same module (sibling files in the same directory) has dropped coverage by more than 5 percentage points relative to its prior state. Detects "I changed file A and broke a test that was covering file B."
- **How to verify:** Compare coverage summary from this branch against the equivalent file on `main`. Diff per-file. Any file with a drop > 5pp triggers a flag.
  - **Optimization:** If a recent main coverage report is cached locally, reuse it.
- **Pass evidence example:** "Sibling-file coverage stable; max delta was -1.2pp."
- **Fail evidence example:** "`services/foo/index.ts` dropped from 47% to 31% — a -16pp regression. Probably a test was deleted or skipped."
- **Skip allowed:** Mark PARTIAL with a note if the prior coverage baseline isn't available locally (e.g., first-time run with no main baseline cached). Do NOT mark FAIL on missing baseline.

### 4. Test files are not skipped
- **Statement:** No new `describe.skip`, `it.skip`, `test.skip`, or `xit(`/`xdescribe(` introduced in the diff. Skipping defeats the rubric.
- **How to verify:**
  ```bash
  git diff main..HEAD -- '<your-test-glob>' | grep -E '^\+.*\b(describe|it|test)\.skip\b|^\+.*\bx(it|describe)\('
  ```
  Any output means new skips were added — fail.
- **Pass evidence example:** "Diff introduces 0 new test skips."
- **Fail evidence example:** "Test file adds `it.skip('rate limit kicks in', ...)` — must un-skip before merge."
- **Allowed exception:** Conditional skips like `it.skipIf(condition)` are permitted when the condition is a real environmental gate (e.g., `skipIf(!process.env.STRIPE_SECRET_KEY)` for SaaS-only billing tests). Document the reason in a top-of-file comment. The grader should accept these but call them out as a Note.

## Notes for the grader

- Run with coverage only — don't try to run integration tests that need external infrastructure. The coverage rubric is a unit-test gate.
- If coverage tooling itself fails (e.g., missing dependency), surface that as a PARTIAL with a setup note. Don't mark FAIL on missing tooling.
- Pair with `feature-complete` for new routes/services. Pair with `route-compliance` for new routes specifically.
- The thresholds in the table can be tightened over time. When the floor moves up, leave the OLD floor here in a comment for one release cycle so existing in-flight branches don't all become FAIL overnight.

## Revision history

- <YYYY-MM-DD> — initial draft
