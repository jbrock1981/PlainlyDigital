# Rubric: pr-ready

**When to apply:** Use to grade whether a branch is ready to open as a PR for review (or merge for solo-dev work). Lighter than `feature-complete` — focuses on what the reviewer / future-you will need.

**Verdict thresholds:**
- PASS: every criterion PASS
- PARTIAL: PASS/PARTIAL mix, no FAIL
- FAIL: any FAIL, or more than half PARTIAL

## Criteria

### 1. Commits are clean
- **Statement:** Either a single squash-able commit, OR meaningful atomic commits. No "wip", "fix", "asdf" messages on the final state.
- **How to verify:** `git log --oneline main..HEAD` (or `git log --oneline -10` if working on main).
- **Pass evidence example:** "3 commits, each with conventional-style message: `feat(api): add foo route`, `test(api): cover foo route 401 path`, `docs: note new env var`."
- **Fail evidence example:** "12 commits including 'wip', 'fix typo', 'try again', 'fix again'."

### 2. Self-review pass
- **Statement:** Walkthrough of `git diff <base>..HEAD` reveals no leftover debugging code, no commented-out code, no obvious typos, no TODO without a tracking link.
- **How to verify:** Read the diff. Grep for `console.log`, `TODO`, `FIXME`, `XXX`, `debugger`.
- **Pass evidence example:** "Diff is purposeful; one TODO references an issue tracker."
- **Fail evidence example:** "5 console.log statements in `src/routes/foo.ts`. Two commented-out blocks, 30+ lines."

### 3. PR description quality (if opening a PR)
- **Statement:** PR has a description covering: what changed, why, how to test, anything reviewer should know. For solo merges to main, the merge commit body serves the same role.
- **How to verify:** Read the description / commit body.
- **Pass evidence example:** "Description has Summary / Test plan sections; references the planning doc."
- **Fail evidence example:** "Description is just the branch name, or empty."

### 4. CI / local checks green
- **Statement:** All tests, type checks, lints, and pre-commit checks pass.
- **How to verify:** Run your project's standard pre-merge gauntlet (type-check, unit tests, e2e smoke, lint, pre-commit).
- **Pass evidence example:** "All checks exit 0."
- **Fail evidence example:** "1 unit test failure; linter flags one violation."

### 5. No new secrets in code or history
- **Statement:** No API keys, tokens, passwords, or credentials in the diff or in newly-added files. `.env` not committed; `.env.example` updated with placeholders only when new vars are introduced.
- **How to verify:** Grep diff for common patterns (`sk_`, `Bearer `, `password`, `_KEY=`, `_SECRET=`). Run a secrets scanner if available.
- **Pass evidence example:** "No matches for sensitive patterns; `.env` unchanged; `.env.example` adds placeholders for two new optional vars."
- **Fail evidence example:** "Real test secret appears in `tests/fixtures/oauth.json`."

### 6. Migration safety (if applicable)
- **Statement:** If the diff adds a `.sql` file under your migrations directory, the file uses the next sequential prefix, all DDL is wrapped in `IF NOT EXISTS` / equivalent idempotency guards, and no existing migration was renamed.
- **How to verify:** Inspect the migration file. Run your migration validator if you have one.
- **Pass evidence example:** "Migration follows convention; rerunning the runner is a no-op."
- **Fail evidence example:** "Migration drops a column without an `IF EXISTS` guard; rerun would fail."

## Notes for the grader

- For solo work without a remote PR, treat the merge into main itself as the "PR" and grade the merge commit's diff.
- If the repo doesn't have CI yet, criterion 4 grades against "all local checks listed above were run by the user before merging."

## Revision history

- <YYYY-MM-DD> — initial draft
