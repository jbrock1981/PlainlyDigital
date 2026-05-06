# Outcomes (rubrics)

This folder holds markdown rubrics. Each rubric defines what "done" looks like for a recurring task. The grader subagent (or the Managed Agents API) reads a rubric and scores work against it.

## When to write a rubric

Write a rubric when a task type recurs and "done" has multiple criteria. Examples:

- Shipping a new feature that requires UX, tests, and docs
- Opening a PR that meets the team's review standards
- Deploying to staging or production
- A migration from one library or service to another
- Compliance-sensitive work where criteria must be auditable

You don't need a rubric for one-off changes. Write one when you find yourself thinking "I keep forgetting one of the things this needs."

## Anatomy of a good rubric

A rubric is a list of yes/no testable criteria. The test is: can the grader verify this with code, tests, file inspection, or a build artifact? If not, the criterion is too vague.

**Bad criterion:** "The code is clean."
**Good criterion:** "No function in the new module exceeds 40 lines, verified by linter."

**Bad criterion:** "The feature works."
**Good criterion:** "The auth flow has tests covering: success, expired token, malformed token, missing token. All four pass."

## Files in this folder

- `_template.md` — Copy this when creating a new rubric.
- `feature-complete.md` — Generic "feature is shippable" rubric.
- `pr-ready.md` — PR-readiness rubric.

Add your own as you discover recurring task types. Name them by what they grade, e.g. `oauth-login.md`, `staging-deploy.md`, `compliance-audit.md`.

## Grader vs. advisor — different jobs

- **Grader** scores ONLY what the rubric says. Strict, evidence-based.
- **Advisor** can pressure-test anything, including the rubric itself.

If the grader thinks the rubric is missing a criterion, it surfaces that under "Notes" — it doesn't add criteria silently. To revise the rubric, edit this file directly and re-grade.
