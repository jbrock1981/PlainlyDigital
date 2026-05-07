# Outcomes (rubrics)

This folder holds markdown rubrics. Each rubric defines what "done" looks like for a recurring task. The grader subagent (invoked by `/grade` or `/outcome`) reads a rubric and scores work against it.

## Available rubrics

| Rubric | When to apply |
|---|---|
| `feature-complete.md` | Generic baseline for shippable features |
| `pr-ready.md` | Lighter check before opening a PR / merging |
| `migration-safe.md` | Any change adding a SQL file under your migrations directory |
| `vendor-clean.md` | Customer-facing changes — enforces a no-LLM-vendor-naming convention |
| `dark-theme.md` | Frontend changes — enforces design-token usage |
| `route-compliance.md` | New / modified backend route modules |
| `pre-commit-clean.md` | Composite — runs the full pre-commit suite |
| `page-smoke-test-sync.md` | New frontend pages — every page should have a smoke test |
| `test-coverage-gate.md` | Code changes — enforces minimum line coverage on changed files |

Use `/outcomes` to list these in-session.

## Mapping rubrics to compliance / governance frameworks

A PASS verdict on these rubrics is direct compliance evidence — the rubric's verification commands provide the audit trail. If your project has a compliance framework (CMMC, NIST 800-171, SOC 2, ISO 27001, HIPAA, FedRAMP, etc.), map each rubric to the controls it satisfies.

**Example pattern (illustrative — adapt to your framework):**

| Rubric | CMMC L2 controls satisfied | NIST SP 800-171 |
|---|---|---|
| `vendor-clean` | CM.L2-3.4.3 (configuration change tracking) | 3.4.3 |
| `migration-safe` | CM.L2-3.4.1 (baseline config), CM.L2-3.4.2 (config-change control) | 3.4.1, 3.4.2 |
| `route-compliance` | AC.L2-3.1.1 (account access), AU.L2-3.3.1 (audit events) | 3.1.1, 3.3.1 |
| `pre-commit-clean` | CM.L2-3.4.3 + AC.L2-3.1.1 + AU.L2-3.3.1 (composite) | 3.4.3, 3.1.1, 3.3.1 |
| `feature-complete` | SI.L2-3.14.1 (flaw remediation, when test gate is met) | 3.14.1 |
| `pr-ready` | CM.L2-3.4.3 (configuration tracking) | 3.4.3 |
| `page-smoke-test-sync` | SI.L2-3.14.1 (test coverage for new code) | 3.14.1 |
| `test-coverage-gate` | SI.L2-3.14.1 (flaw remediation), CA.L2-3.12.1 (security assessment) | 3.14.1, 3.12.1 |

The architectural insight is generic: rubric verdicts produce reproducible, evidence-backed records. If your CI pipeline mirrors the same checks, both surfaces feed your evidence-of-record store. Substitute your project's frameworks and controls.

## Workflow

- `/grade <rubric>` — single-shot read-only score
- `/outcome <rubric> <task>` — autonomous loop: implement → grade → on-fail-feed-gaps-back → re-implement, until PASS or max iterations
- `/team <feature>` — full multiagent flow with optional rubric at the end

## When to write a new rubric

Write a rubric when a task type recurs and "done" has multiple criteria. Examples:

- A specific feature surface that recurs (billing, auth, reporting, etc.)
- Compliance-sensitive work where criteria must be auditable
- Deployment / release gates
- Cross-cutting changes (e.g., adding a new integration end-to-end)

You don't need a rubric for one-off changes. Write one when you find yourself thinking "I keep forgetting one of the things this needs."

## Anatomy of a good rubric

A rubric is a list of yes/no testable criteria. The test: can the grader verify this with code, tests, file inspection, or a build artifact? If not, the criterion is too vague.

**Bad criterion:** "The code is clean."
**Good criterion:** "No function in the new module exceeds 40 lines, verified by linter."

**Bad criterion:** "The feature works."
**Good criterion:** "The auth flow has tests covering: success, expired token, malformed token, missing token. All four pass."

## Files in this folder

- `_template.md` — Copy when creating a new rubric.
- The rubrics listed in the table above.

Add your own as you discover recurring task types. Name them by what they grade.

## Grader vs. advisor — different jobs

- **Grader** scores ONLY what the rubric says. Strict, evidence-based.
- **Advisor** can pressure-test anything, including the rubric itself.

If the grader thinks the rubric is missing a criterion, it surfaces that under "Notes" — it doesn't add criteria silently. To revise the rubric, edit the file directly and re-grade.
