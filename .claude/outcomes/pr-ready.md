# Rubric: pr-ready

**When to apply:** Use to grade whether a branch is ready to open as a PR for review (or merge for solo devs). Lighter than feature-complete — focuses on what the reviewer/future-you will need.

**Verdict thresholds:** Same as feature-complete (PASS / PARTIAL / FAIL).

## Criteria

### 1. Commits are clean
- **Statement:** Commit history is readable. Either single squash-able commit OR meaningful, atomic commits. No "wip", "fix", or "asdf" messages on the final state.
- **How to verify:** `git log --oneline main..HEAD`
- **Pass evidence example:** "3 commits, each with descriptive message: 'Add OAuth callback handler', 'Wire OAuth into login UI', 'Tests for OAuth flow.'"
- **Fail evidence example:** "12 commits including 'wip', 'fix typo', 'try again', 'fix again'."

### 2. Branch is up to date with main
- **Statement:** Branch has been rebased or merged with the latest main. No conflicts.
- **How to verify:** `git fetch && git log main..HEAD --oneline` and `git merge-base --is-ancestor main HEAD`
- **Pass evidence example:** "Latest main commit included; clean rebase; no conflicts."
- **Fail evidence example:** "Branch behind main by 17 commits; conflicts in src/auth/."

### 3. Self-review pass
- **Statement:** A walkthrough of `git diff main..HEAD` reveals no leftover debugging code, no commented-out code, no obvious typos, no TODO without an issue link.
- **How to verify:** Read the diff. Grep for `console.log`, `TODO`, `FIXME`, `XXX`, `debugger`.
- **Pass evidence example:** "Diff is purposeful; one TODO with issue link to #134."
- **Fail evidence example:** "5 console.log statements in src/auth/. Two commented-out blocks 30+ lines."

### 4. PR description quality
- **Statement:** The PR has a description covering: what changed, why, how to test, anything reviewer should know.
- **How to verify:** Read the description (or commit message if no PR body yet).
- **Pass evidence example:** "Description has 'What' / 'Why' / 'How to test' sections, references the planning doc."
- **Fail evidence example:** "Description is just the branch name."

### 5. CI green (or local equivalent)
- **Statement:** All tests, type checks, lints, and build steps pass.
- **How to verify:** Run them, or check CI status.
- **Pass evidence example:** "GitHub Actions green; local `npm test` exits 0."
- **Fail evidence example:** "1 test failing; lint warnings count went up by 12."

### 6. No new secrets in code or history
- **Statement:** No API keys, tokens, passwords, or credentials in the diff or in newly added files.
- **How to verify:** Grep diff for common secret patterns (`sk_`, `Bearer `, `password`, etc.). Run a secrets scanner if available.
- **Pass evidence example:** "No matches for sensitive patterns; .env unchanged; .env.example updated with placeholder only."
- **Fail evidence example:** "Real ANTHROPIC_API_KEY appears in tests/fixtures/auth.json."

## Notes for the grader

- For solo work without a remote PR, treat the merge into main itself as the "PR" and grade what's in the merge commit's diff.
- If the repo doesn't have CI, criterion 5 grades against "all local checks run by the user before merging" — verify by asking which were run.

## Revision history

- 2026-05-06 — initial draft
