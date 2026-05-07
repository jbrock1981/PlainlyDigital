# Rubric: dark-theme

**When to apply:** Any change to your frontend source files (e.g., `web/src/`, `platform/src/`, `app/`) — pages, components, layouts. Quick rubric to enforce a dark-theme-only convention before merge.

**Why this rubric exists:** Some projects are dark-theme-only. Light-theme Tailwind classes that slip in cause a jarring visual regression in production. A project-specific dark-theme-enforcer (lint rule or AST script) catches the obvious cases; this rubric layers on intent-level checks the linter can't catch (e.g., a "white card on a black background" that uses `bg-white` instead of the right design token).

**If your project supports both light and dark themes (or only light), delete or rewrite this rubric.**

**Configure for your project:**
- `<your-prefix>` — your project's design-token Tailwind prefix (e.g., `text-acme-text`, `bg-acme-surface`). Set this in your `tailwind.config.ts` and reference it consistently.
- `<frontend-src-glob>` — glob for your frontend source (e.g., `web/src/**/*.{tsx,ts}`).

**Verdict thresholds:** PASS / PARTIAL / FAIL per the standard rules.

## Criteria

### 1. No light-theme Tailwind classes in changed files
- **Statement:** No use of `text-gray-900`, `text-gray-800`, `bg-gray-50`, `bg-gray-100`, `bg-white`, `border-gray-200`, or any other Tailwind class that assumes a light background.
- **How to verify:** Run your project's dark-theme-enforcer if one exists. Otherwise: `git diff --name-only main..HEAD -- '<frontend-src-glob>' | xargs grep -E '(text|bg|border)-(white|black|gray-|slate-|zinc-|neutral-|stone-)\d*'`.
- **Pass evidence example:** "Enforcer reports clean across all changed files."
- **Fail evidence example:** "Enforcer flags `text-gray-900` in `<frontend-src>/dashboard/foo/page.tsx:42`."

### 2. Project design tokens used for color
- **Statement:** Color, background, and border tokens use the project palette (`text-<your-prefix>-text`, `bg-<your-prefix>-surface`, `border-<your-prefix>-border`, etc.) rather than raw Tailwind colors.
- **How to verify:** Inspect changed files. Grep for `text-` / `bg-` / `border-` followed by raw color names (`white`, `black`, `slate-`, `zinc-`, `neutral-`, `gray-`, `stone-`).
- **Pass evidence example:** "All color usage routes through `<your-prefix>-*` tokens. Where a raw hex is needed, it's in a tailwind.config.ts entry, not inline."
- **Fail evidence example:** "Inline `bg-zinc-800` and `text-slate-200` in a card component."

### 3. New components reuse text-contrast tokens
- **Statement:** New visual components route primary text through `text-<your-prefix>-text`, secondary/muted text through `text-<your-prefix>-muted` (or another `text-<your-prefix>-*` token), and interactive states through the corresponding hover/focus tokens. No raw `text-gray-*`, `text-slate-*`, `text-zinc-*`, `text-neutral-*`, `text-stone-*`, `text-white`, `text-black` in new JSX.
- **How to verify:** On the diff for `<frontend-src-glob>`, grep for raw text-color utilities. Any hit in added lines is a fail. Then grep added JSX for `text-<your-prefix>-` to confirm tokens ARE present in new color-bearing markup.
  - `git diff main..HEAD -- '<frontend-src-glob>' | grep -E '^\+.*text-(gray|slate|zinc|neutral|stone)-[0-9]+|^\+.*text-(white|black)\b'` — must return zero lines.
  - `git diff main..HEAD -- '<frontend-src-glob>' | grep -E '^\+.*className.*text-<your-prefix>-'` — informational; confirms new components opt in to the palette.
- **Pass evidence example:** "Diff shows N new lines adding `text-<your-prefix>-text` / `text-<your-prefix>-muted` and 0 lines adding raw Tailwind text-color utilities."
- **Fail evidence example:** "Line +42 in `<frontend-src>/dashboard/foo/page.tsx` adds `text-gray-500` — must be `text-<your-prefix>-muted`."

> **Grader note (not a gating criterion):** Dark-mode legibility is partly subjective (contrast ratios, semantic role). The token check above is the deterministic gate. If you spot a token combination that *technically* passes but visually misuses contrast (e.g., the muted token used for primary content), call it out in the report — but do NOT downgrade the verdict. Surface for human review instead.

### 4. No hardcoded white/light hex codes
- **Statement:** No `#fff`, `#ffffff`, `#fafafa`, `rgb(255, 255, 255)`, etc. hardcoded inline. If light hex is genuinely needed (e.g., for a chart axis), it should be defined in `tailwind.config.ts` as a named token.
- **How to verify:** Grep diff for hex/rgb patterns matching white/near-white.
- **Pass evidence example:** "No inline hex colors; all colors flow through tailwind tokens."
- **Fail evidence example:** "Inline `style={{ color: '#fff' }}` in a list component."

## Notes for the grader

- The dark-theme-enforcer script (if your project has one) is the primary check. This rubric supplements it with intent-level questions the script can't answer.
- Charts and SVG fills are an exception only when defined as named tokens (the chart library needs raw hex; that's fine if the hex is centralized).
- Mark PARTIAL rather than FAIL if violations are limited to a single isolated file — likely a quick fix.

## Revision history

- <YYYY-MM-DD> — initial draft
