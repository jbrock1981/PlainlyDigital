# Rubric: vendor-clean

**When to apply:** Any change that touches customer-facing code, UI strings, docs, or marketing copy in a project that has a no-LLM-vendor-naming convention. This rubric enforces "never reference LLM vendors by name in customer-facing surfaces," with explicit carve-outs for AI-transparency surfaces required by compliance frameworks (NIST AI RMF, ISO 42001, EU AI Act, etc.).

**Why this rubric exists:** A BYOAI / vendor-agnostic positioning is undermined by stray vendor names in customer surfaces. Some surfaces (Model Card, Use Case Assessment, Trust page, BYOAI bootstrap, AI provenance badges) MUST name vendors per regulatory requirements — those are explicit carve-outs your project should enumerate in CLAUDE.md.

**If your project doesn't have a vendor-naming convention, delete this rubric.** It's only useful for projects that intentionally avoid naming AI vendors in customer surfaces.

**Verdict thresholds:** PASS / PARTIAL / FAIL per the standard rules.

## Criteria

### 1. No vendor names in non-carve-out customer surfaces
- **Statement:** No LLM vendor name (Anthropic, OpenAI, Claude, GPT, ChatGPT, Gemini, Bedrock, Mistral, Cohere, etc.) appears in customer-facing code, UI strings, error messages, dashboard pages, marketing pages, or docs OUTSIDE the documented carve-outs.
- **How to verify:** Run a project-specific vendor-scrubber if you have one. Otherwise: `grep -rin "anthropic\|openai\|gpt-4\|claude-\|gemini\|bedrock\|mistral\|cohere" <your-frontend-src>/ <your-backend-src>/ docs/ --exclude-dir=node_modules`.
- **Pass evidence example:** "No vendor matches across changed files."
- **Fail evidence example:** "`<frontend-src>/dashboard/scanner/page.tsx:142` includes the string 'Powered by Claude.' Not a carve-out file."

### 2. Carve-out files still name vendors as required
- **Statement:** The carve-out surfaces continue to name vendors (this is REQUIRED by the carve-out, not optional). Enumerate your carve-out files in CLAUDE.md. Common examples:
  - Model Card pages (regulatory requirement to name model behind AI outputs)
  - Use Case Assessment forms
  - Public Trust / Governance pages
  - AI provenance badges / inline attribution components
  - First-launch BYOAI bootstrap (customer picks their LLM vendor at install)
- **How to verify:** Read each carve-out file. Confirm vendor naming is still present (a refactor that "cleaned up" a carve-out by removing vendor names is a regression — it breaks the regulatory requirement).
- **Pass evidence example:** "Trust page still names supported BYOAI providers in the AI Governance section. AI provenance badge still surfaces provider/model from the provenance record."
- **Fail evidence example:** "Diff removed the provider name display in `AiOutputBadge.tsx` — this regresses NIST AI RMF / EU AI Act compliance."

### 3. Logger statements don't leak vendor names through customer-visible error paths
- **Statement:** Server-side logger statements MAY include vendor names for internal observability, but any error message that surfaces to the customer (HTTP response body, UI error toast, audit log entry visible to the customer) must use generic language ("the configured AI provider", "your selected model").
- **How to verify:** Trace error-handling code paths. Look at `res.status(...).json({ error: ... })` calls and frontend error toasts. Check audit log entries that customers can read.
- **Pass evidence example:** "Errors surfaced to customer say 'AI provider returned an error'; the underlying provider name is in `logger.error` but not in the response body."
- **Fail evidence example:** "`res.status(500).json({ error: 'Anthropic API timeout' })` — leaks vendor through HTTP response."

### 4. New AI features wire AI provenance correctly
- **Statement:** Any new code path that produces an AI output writes a row into your project's provenance table (e.g., `ai_provenance`) so the inline provenance badge can render the provider/model. This is the regulatory carve-out's load-bearing mechanism.
- **How to verify:** Check your project's AI provenance service. Confirm new AI-output endpoints call into it.
- **Pass evidence example:** "New endpoint `/api/ai/foo` calls `recordProvenance({ provider, model, ... })` after each LLM call. Verified by integration test."
- **Fail evidence example:** "New endpoint produces AI output but no provenance write. Provenance badge will show 'unknown' for these outputs."

## Notes for the grader

- The carve-outs should be deliberately narrow and enumerated in CLAUDE.md. If a future surface argues "we should name vendors here too," that's a CLAUDE.md change, not a quiet rubric exception.
- A project-specific vendor-scrubber script (AI-powered or grep-based) is the primary check; manual grep is a backup for situations where the script fails or hasn't been run.
- Brand names of AI products (e.g., "Bedrock", "Vertex AI") count as vendor names for this rubric.
- Internal staff-only pages are technically not customer-facing, so naming the vendor in staff tooling may be OK. The rubric grades customer-facing surfaces only.

## Revision history

- <YYYY-MM-DD> — initial draft
