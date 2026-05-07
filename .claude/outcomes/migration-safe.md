# Rubric: migration-safe

**When to apply:** Any change that adds or modifies a SQL file under your project's migrations directory (e.g., `db/migrations/`, `api/src/db/migrations/`, `prisma/migrations/`, etc.). Use after writing the migration but before merging — `/outcome migration-safe --git HEAD` is a typical invocation.

**Why this rubric exists:** Many migration runners track applied migrations by **filename**, not by number prefix. Renaming an existing migration causes it to re-apply. Non-idempotent DDL fails on rerun. Both classes of bug are subtle and have bitten in the past.

**Verdict thresholds:** PASS / PARTIAL / FAIL per the standard rules.

## Criteria

### 1. Sequential numbering
- **Statement:** New migration filename uses the next available numeric prefix (or follows your project's naming convention — timestamps, ULIDs, etc.). Two files sharing a prefix may be allowed if your runner applies them alphabetically — but a new migration should use the next free number unless intentionally bundling with an existing prefix.
- **How to verify:** `ls <your-migrations-dir>/ | sort | tail -5` and confirm the new file follows. Run your project's migration validator if one exists.
- **Pass evidence example:** "Latest before this PR was `0289-foo.sql`; new file is `0290-bar.sql`."
- **Fail evidence example:** "Skipped from `0289-` to `0295-` with no explanation, or renamed `0288-baz.sql` → `0288-baz-v2.sql` (which would cause re-application)."

### 2. Idempotent on rerun
- **Statement:** Every DDL statement is wrapped in `IF NOT EXISTS` (for `CREATE`) / `IF EXISTS` (for `DROP`) / `DO $$ BEGIN ... EXCEPTION WHEN duplicate_*` blocks (for `ALTER` operations that lack a built-in idempotency clause), or your stack's equivalent guards.
- **How to verify:** Read the migration. For each `CREATE TABLE`, `CREATE INDEX`, `CREATE TYPE`, `ADD COLUMN`, etc., confirm the appropriate guard. Then conceptually rerun: would applying this twice succeed?
- **Pass evidence example:** "All `CREATE TABLE` statements use `IF NOT EXISTS`. The `ALTER TYPE ... ADD VALUE` is wrapped in a `DO $$` block that catches `duplicate_object`."
- **Fail evidence example:** "`CREATE TABLE foo (...)` without `IF NOT EXISTS`. `ALTER TABLE bar ADD COLUMN baz int NOT NULL DEFAULT 0` would fail on rerun if the column already exists."

### 3. Backward-compatible with running production
- **Statement:** The migration can apply to a live database without breaking the currently-deployed application code. Specifically: no destructive renames, no dropping columns the running code still reads, no NOT NULL adds without a backfill default for existing rows.
- **How to verify:** Cross-reference the migration with the diff in `src/`. If a service reads a column the migration drops, the deployment ordering is broken. For NOT NULL adds, confirm a default value exists OR that the migration backfills existing rows in a separate step.
- **Pass evidence example:** "Adds a new nullable column; running code doesn't reference it yet."
- **Fail evidence example:** "Drops `users.legacy_token`; service `auth.ts:42` still reads it."

### 4. No pre-existing migrations renamed
- **Statement:** No file currently in the migrations directory was renamed in this diff.
- **How to verify:** `git diff --name-status main..HEAD -- <your-migrations-dir>/` — flag any `R` (rename) entries.
- **Pass evidence example:** "Only `A` (add) entries; no renames."
- **Fail evidence example:** "Renamed `0079-foo.sql` → `0079-bar.sql`. The runner would re-apply it on next deploy and fail / corrupt state."

### 5. Migration validator clean (if your project has one)
- **Statement:** Your project's migration validator passes without errors.
- **How to verify:** Run the command (e.g., `<your migration validator>`).
- **Pass evidence example:** "Validator output: 'All N migrations valid.'"
- **Fail evidence example:** "Validator flags missing `IF NOT EXISTS` on line 14."

### 6. Destructive operations are reviewed
- **Statement:** If the migration includes any `DROP TABLE`, `DROP COLUMN`, `DROP INDEX`, `TRUNCATE`, or `DELETE FROM` (without a strict `WHERE` that bounds the impact), the rubric requires explicit human acknowledgement that the destructive op is intended. The grader marks this PARTIAL by default; the human flips it to PASS only after confirming.
- **How to verify:** Grep for `DROP `, `TRUNCATE`, `DELETE FROM` in the migration. If found, mark PARTIAL and surface for human review.
- **Pass evidence example:** "No destructive operations." OR "Drop reviewed and acknowledged in commit body: 'Drop legacy_sessions — superseded by sessions_v2 (deployed 2026-04-01).'"
- **Fail evidence example:** "`DROP TABLE legacy_sessions` with no acknowledgement and the running app may still reference it."

## Notes for the grader

- The `IF NOT EXISTS` requirement is non-negotiable for this rubric.
- If a migration is part of a bundle (e.g., two files sharing a prefix to land together), confirm both files individually and note the bundle relationship under "Notes."
- For migrations that add database extensions (e.g., `pgvector`, `pg_trgm`), the extension should be created with `CREATE EXTENSION IF NOT EXISTS` in the same migration.

## Revision history

- <YYYY-MM-DD> — initial draft
