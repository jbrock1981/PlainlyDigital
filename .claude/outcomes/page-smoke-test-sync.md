# Rubric: page-smoke-test-sync

**When to apply:** Any change that adds or moves a frontend page file in your project (`<frontend-pages-glob>`, e.g. `web/src/app/**/page.tsx`, `pages/**/*.tsx`, `src/routes/**/*.svelte`). Enforces "every new page must have a smoke render test."

**Why this rubric exists:** New pages are the dominant unit of frontend growth in many projects. Without an automated gate, "I forgot the smoke test" sneaks in. The pre-commit suite typically doesn't enforce test pairing — this rubric closes that loop and serves as a load-bearing check during E2E coverage runways.

**Configure for your project:**
- `<frontend-pages-glob>` — glob for your frontend pages (e.g., `web/src/app/**/page.tsx`).
- `<smoke-tests-dir>` — directory for smoke tests (e.g., `web/tests/e2e/smoke/`).
- `<test-helpers-dir>` — directory for shared test helpers (e.g., `web/tests/e2e/helpers/`).

**Verdict thresholds:** PASS / PARTIAL / FAIL per the standard rules.

## Criteria

### 1. Every new page file has a corresponding smoke test entry
- **Statement:** For each new page file matching `<frontend-pages-glob>` introduced in the diff, a smoke test exists in `<smoke-tests-dir>` that exercises the page's route. The test must (a) navigate to the route, (b) assert the page renders without error, and (c) assert at least one stable selector / heading / data-testid is present.
- **How to verify:**
  ```bash
  # Find new page files in the diff
  NEW_PAGES=$(git diff --diff-filter=A --name-only main..HEAD -- '<frontend-pages-glob>')
  for PAGE in $NEW_PAGES; do
    # Derive route from path (strip the framework's app-prefix and page-suffix)
    ROUTE=$(echo "$PAGE" | sed -E 's|^<your-app-prefix>||; s|/page\.tsx$||')
    # Search smoke tests for the route
    if ! grep -rq "$ROUTE" <smoke-tests-dir>/; then
      echo "FAIL: no smoke test references route $ROUTE (page $PAGE)"
    fi
  done
  ```
- **Pass evidence example:** "Diff adds `<frontend-src>/dashboard/foo/page.tsx`; smoke test `<smoke-tests-dir>/dashboard-foo.spec.ts` references route `/dashboard/foo` and asserts the page heading."
- **Fail evidence example:** "Diff adds `<frontend-src>/dashboard/foo/page.tsx`; no file under `<smoke-tests-dir>/` references the route `/dashboard/foo`."

### 2. The smoke test uses the canonical helpers
- **Statement:** Smoke tests import from `<test-helpers-dir>` (auth, navigation, fixtures, API helpers) instead of inlining ad-hoc setup. Per your project's testing conventions, demo credentials should come from helpers, not be hardcoded.
- **How to verify:** For each smoke spec touched in the diff, grep for `from.*<test-helpers-dir>` import. Ad-hoc `page.goto('/login'); await page.fill(...)` blocks count as failure unless the spec is intentionally bypassing helpers (must say so in a top-of-file comment).
  ```bash
  git diff main..HEAD --name-only -- '<smoke-tests-dir>/*.spec.ts' | xargs -I{} grep -L "<test-helpers-dir>" {} 2>/dev/null
  ```
  Any path returned is a fail (it's a smoke spec that does NOT use the helpers).
- **Pass evidence example:** "All new/modified smoke specs import auth + navigation helpers from `<test-helpers-dir>`."
- **Fail evidence example:** "`<smoke-tests-dir>/dashboard-foo.spec.ts` does not import from helpers/ — uses inline `page.goto('/login')` setup."

### 3. The smoke test runs green
- **Statement:** Running the new/modified specs locally against a running app produces a green pass.
- **How to verify:**
  ```bash
  <your e2e command> <smoke-tests-dir> --grep "<page name keyword>"
  ```
  Exit code 0 with all specs passing = PASS. Any failure = FAIL.
- **Pass evidence example:** "Test runner reports `5 passed (12.3s)` for the new specs."
- **Fail evidence example:** "Spec timeout: page `/dashboard/foo` never settled — likely missing data-testid or unmounted async state."
- **Skip allowed:** If the dev server isn't running locally (no `localhost:<your-dev-port>` reachable), grade this PARTIAL with a note that CI will catch it. Do NOT mark FAIL on an unreachable test runner.

### 4. Renamed/moved pages keep their smoke test in sync
- **Statement:** If a page was moved (path changed), the corresponding smoke test's route assertion must also be updated. A stale smoke test pointing at the old path is a FAIL.
- **How to verify:** For each `R<NN>` (rename) entry in `git diff --diff-filter=R --name-status main..HEAD`, grep smoke tests for the OLD route. Any hit is a stale reference.
- **Pass evidence example:** "Move `dashboard/old-foo/page.tsx` → `dashboard/foo/page.tsx`; smoke test updated to assert `/dashboard/foo`."
- **Fail evidence example:** "Page moved to `/dashboard/foo` but `dashboard-foo.spec.ts` still references `/dashboard/old-foo`."

## Notes for the grader

- This rubric does NOT apply to layout, route group, loading, error, or not-found special files. Only top-level page files (and API route handlers if you want to extend it later).
- If the diff includes 5+ new pages, the grader may sample (verify 3 at random) and surface the rest as "needs spot-check." Mark PARTIAL if the sample is clean but coverage is uncertain.
- Pair this rubric with `feature-complete` for routes that include backend changes — page-smoke-test-sync only covers the frontend half.
- When run inside an `/outcome` autonomous loop, the implementer should add the smoke test in the same iteration that adds the page; do NOT defer to a "test PR follow-up" — that pattern is what this rubric is designed to catch.
- **`gotoAndAssertNoCrash` vs `gotoAndAssertRender` decision rule:** Use `gotoAndAssertRender` (or your project's equivalent strict assertion) when the page's `<h1>` (or other stable selector) renders unconditionally. Use the weaker no-crash assertion when the heading is data-gated (only renders if a record was found) or when the page is for a parametric ID that won't resolve in test data — the error-boundary `data-testid` arm of criterion 1 still satisfies the rubric. If a spec uses the no-crash helper everywhere unnecessarily, that's a weaker assertion than the rubric prefers — call it out as a Note.

## Revision history

- <YYYY-MM-DD> — initial draft
