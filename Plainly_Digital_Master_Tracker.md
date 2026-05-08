# Plainly Digital LLC — Master Business Tracker

**Last Updated:** 2026-04-17
**Owner:** Jonathan Brock
**Entity:** Plainly Digital LLC (Tennessee LLC, EIN: 41-4877857, DUNS: 144377444)

---

## Products Under Plainly Digital LLC

| Product | Repo | Stack | Deploy | Status |
|---------|------|-------|--------|--------|
| **Plainly** (finlit) | jbrock1981/Plainly | React Native (Expo 55) + Express + Neon PG | Vercel + Render + Neon | ~75% complete, pre-beta |
| **Vinla** (health) | jbrock1981/vytally | React Native (Expo 53) + Zustand + Supabase + SQLite | Vercel + Supabase | ~70% complete, family beta |
| **Notch** (life advisor) | jbrock1981/42ly | React Native (Expo 55) + Express + Supabase PG | Vercel (notch.vercel.app + notch-api.vercel.app) | MVP complete, invite beta |
| **Winlet** (wins) | jbrock1981/Accomplishly | React Native (Expo 53) + Express + Neon PG + Vite web | Render (API) + Vercel (web) | Feature complete, deployed |
| **Fraus** (AI scam detector) | jbrock1981/Scamly (private; rename pending) | Next.js 14 (landing) → Phase 2: Express + Neon + Expo | Pending Vercel | **Phase 1 landing scaffold only (2026-04-17)** — not deployed, no MVP |
| **Pillarly** (senior medication assistant) | jbrock1981/Pillarly (private) | Next.js 14 (landing) → Phase 2: Express + Neon + Expo | Pending Vercel | **Phase 1 landing scaffold only (2026-04-17)** — not deployed, no MVP |

---

## Shared Architecture

### Sage AI (Three-Layer System)
All apps share the same AI personality brand:
- **Layer 1 (Shared):** Brand personality — tone, values, communication style (docs/SAGE-BRAND-PERSONALITY.md)
- **Layer 2 (App-specific):** Domain expertise per app
- **Layer 3 (Per-user):** Personalization, conversation history, user context

### Shared Pricing Model
| Tier | Price | AI Model | Daily Cap | Monthly Cap |
|------|-------|----------|-----------|-------------|
| Free | $0 | Haiku 4.5 | 10 | 60 |
| Pro | $2.99/mo ($24.99/yr) | Haiku 4.5 | 40 | 500 |
| Pro+ | $6.99/mo ($57.99/yr) | Sonnet 4.6 (50/mo cap) | 80 | 1,200 |
| Boost Pack | $1.99 | — | +50 calls | — |
| Power Boost | $4.99 | — | +200 calls | — |

### Shared Safety
- Crisis detection (55+ patterns, unicode/homoglyph/l33tspeak protection)
- Input guardrails (prompt injection, jailbreak, role override)
- Output guardrails (medical/legal/financial boundary checks)
- AI disclosure badges on all AI responses
- Per-user cost guard (tier-based daily/monthly limits)

---

## Product Details

### Plainly (Financial Literacy for Gen Z)
- 18 modules, 121 lessons, ~242 quiz cards
- Plaid integration (real spending data)
- Money Personality quiz, Financial Health Score, Money Roast
- TikTok-style personalized feed
- Certification system (50-question assessment, public verification)
- i18n: English + Spanish
- ⚠️ **Test suite regressed (2026-04-11):** App Jest cannot run (missing `typescript` devDep — 0/31 suites execute). Server Jest has 1 broken suite (workflows.test.ts → pdf-parse DOMMatrix crash), 65 tests pass. CLAUDE.md claim of "509 tests passing" is currently false.
- **Blockers:** RevenueCat not integrated, Plaid env vars not configured on Render, App Store credentials empty
- **Audit findings (2026-04-11):** 17 verified issues — 3 Critical, 9 High, 5 Medium. See `USER_TESTING_FINDINGS_2026-04-11.md` for details and `CLI_PROMPTS_TO_FIX_FINDINGS.md` for ready-to-paste CLI tasks.

#### Plainly Pre-Beta Issue Todo (2026-04-11 audit)

**Critical — must fix before any user sees the app:**
- [ ] **C1** — App Jest broken: add `typescript` to app/devDependencies, re-run `npm test`, update CLAUDE.md test count
- [ ] **C2** — `DELETE /me` doesn't revoke Plaid items (server/src/routes/auth.ts:285) — runaway Plaid billing after account deletion
- [ ] **C3** — `workflows.test.ts` crashes server Jest via `pdfjs-dist` DOMMatrix — defer pdf-parse import

**High — fix before beta launch:**
- [ ] **H1** — Validate `JWT_SECRET` length ≥ 32 at startup (server/src/middleware/auth.ts:5)
- [ ] **H2** — Cost-guard check-then-act race condition (server/src/lib/cost-guard.ts:231) — rewrite as atomic `UPDATE ... WHERE ... RETURNING`
- [ ] **H3** — Login timing leak reveals valid emails (server/src/routes/auth.ts:149) — run dummy bcrypt on non-existent email
- [ ] **H4** — Registration race between SELECT and INSERT (server/src/routes/auth.ts:105) — use `INSERT ON CONFLICT`
- [ ] **H5** — Pro+ Sonnet 50/month cap defined but never enforced (cost-guard.ts:73 + coach.ts:83) — potential $72/mo AI cost vs $6.99 revenue
- [ ] **H6** — Cost guard fails OPEN to free tier on DB error (cost-guard.ts:250) — fail closed with cached tier
- [ ] **H7** — Feed endpoint undercounts AI calls: 1 guard check but 2 Claude calls on Mondays (feed.ts:349)
- [ ] **H8** — Coach stream doesn't abort on client disconnect (coach.ts:138) — wasted Anthropic tokens
- [ ] **H9** — Output guardrails checked AFTER `[DONE]` sent (coach.ts:154) — users see bad content before filter

**Medium — first post-beta sprint:**
- [ ] **M1** — User name injected raw into system prompt intro template (system-prompt.ts:104)
- [ ] **M2** — `JSON.parse` without try/catch crashes profile screen (profile.tsx:44)
- [ ] **M3** — Cost counter increments by fixed +1 regardless of real tokens used (cost-guard.ts:357)
- [ ] **M4** — Cost guard daily reset uses UTC only (cost-guard.ts:262)
- [ ] **M5** — `useSubscription` hardcoded to `pro_plus` default (useSubscription.ts:52) — also trusts client, not server

**Verified NOT bugs (agents were wrong):** Crisis banner API blocking (already correct), "kill this debt" false positive (regex actually requires "myself"/"my life"), voice input bypass (routes through full pipeline), affiliate `/redirect` no-auth (intentional deep link, UID already hashed), webhook 200-on-error (Plaid retry policy requires it).

### Vinla (AI Health Intelligence)
- Food/water/sleep/mood/exercise logging
- AI photo food recognition (Claude Vision)
- Deep nutrient tracking (USDA FoodData Central, 29 nutrients)
- Cross-domain intelligence (correlations, patterns, forecasts)
- PHQ-2/GAD-2 screening, Gentle Mode
- Bloom virtual garden, Vinla Wrapped
- 290 tests passing (14 suites), TS clean
- **Blockers:** Data still in local SQLite (need Supabase sync), no payment processor, no age gate
- **Audit findings (2026-04-11):** 17 verified issues — 3 Critical, 9 High, 5 Medium, 2 Low. See `USER_TESTING_FINDINGS_2026-04-11.md` for details and `CLI_PROMPTS_TO_FIX_FINDINGS.md` for ready-to-paste CLI tasks (both in Vinla repo).

#### Vinla Family-Beta Issue Todo (2026-04-11 audit)

**Critical — must fix before expanding beta:**
- [ ] **C1** — Client owns the AI system prompt end-to-end (api/chat.ts:26 accepts `system` from body); any user can bypass all Sage personality + guardrails. Move prompt assembly server-side.
- [ ] **C2** — `maxSonnetCallsPerMonth = 50` defined but never enforced; api/chat.ts:95 hardcodes Sonnet for every tier. Free/Pro users get $0.06/call instead of $0.005/call (12x cost overrun); Pro+ has no cap.
- [ ] **C3** — Cost guard check-then-act race (cost-guard.ts:104-202) — same bug shape as Plainly H2; needs atomic `UPDATE ... WHERE ... RETURNING`.

**High — fix before expanding beta:**
- [ ] **H1** — Chat stream doesn't abort on client disconnect (api/chat.ts:82-126) — wasted Sonnet tokens.
- [ ] **H2** — Output guardrails are a dead no-op: api/chat.ts:108-115 runs the check, then the `if (!outputCheck.passed)` branch is literally empty. No log, no block, no banner. Feature documented but completely absent at runtime.
- [ ] **H3** — Login timing side channel (api/auth/login.ts:25-38) — bcrypt skipped on unknown email; run dummy hash.
- [ ] **H4** — Registration race (api/auth/register.ts:39-65) — SELECT then INSERT; use `ON CONFLICT`.
- [ ] **H5** — `JWT_SECRET` existence-only check duplicated in 6 files; no length validation. Centralize via `api/_lib/jwt.ts`.
- [ ] **H6** — Rate limiter (`api/_lib/rate-limit.ts`) fully defined + exported but never imported anywhere. Auth endpoints have zero brute-force protection.
- [ ] **H7** — `buildMoodAdaptiveContext` defined at src/ai/context.ts:188 but never called; mood-adaptive tone feature silently doesn't exist.
- [ ] **H8** — PHQ-2/GAD-2 screening UI collects + computes scores but `handleSubmit` never persists them; no trend, no coach awareness.
- [ ] **H9** — Module-level `contextCache` in src/ai/context.ts:23 not keyed by user and not cleared on logout — PHI leakage risk on shared devices (family mode).

**Medium — first post-beta sprint:**
- [ ] **M1** — 7 Zustand stores parse persisted JSON with no try/catch (social/target/streak/milestone/profile/subscription/notification/wearable).
- [ ] **M2** — `getAllChatMessages` unbounded — add default limit.
- [ ] **M3** — `estimateCostCents` hardcoded for Sonnet pricing regardless of model.
- [ ] **M4** — `/api/insights` trusts client-supplied `model` hint; free/pro can force Sonnet.
- [ ] **M5** — Zustand stores have no schema version migration; breaking changes silently carry stale state.

**Low — backlog:**
- [ ] **L1** — Cost guard DB errors swallowed silently; add console.error for observability.
- [ ] **L2** — Food vision adversarial photo text partially mitigated by schema validation; revisit if web export ships.

**Verified NOT bugs (agents were wrong):** authStore.ts JSON.parse IS wrapped in try/catch; insights endpoint returns plain text not JSON (no parse bug); crisis detection ED patterns ARE complete (purge/fast/starve/laxatives covered); classifyCrisisWithAI retry would add latency for no safety benefit (current fallback to 'concerning' is correct); prompt caching in chat.ts is correctly wrapped in ephemeral cache_control.

### Notch (AI Life Advisor)
- 6 life domains: Career, Relationships, Finances, Health, Personal Growth, Purpose
- Decision Engine with scenario modeling
- Persistent Memory with growth timeline
- Action Quest system
- Personality training (12-question calibration, unique to Notch)
- 718 tests (318 app + 400 server)
- **Blockers:** Parental consent flow incomplete, no Privacy Policy/ToS, DBA not registered

### Winlet (Personal Wins Tracker)
- Quick-capture wins, timeline, calendar heatmap
- Lift Me Up (random past win surfacing)
- Life Resume + Year in Review (Claude narratives)
- Team/family spaces with invite codes
- Shareable win cards (4 templates)
- Slack kudos auto-capture, email forwarding
- Web companion (Vite + React)
- 379 tests (229 server + 125 mobile + 25 web), TS clean across app/server/web
- **Baseline health (2026-04-11):** app 14/14 suites green (166 tests), web TS clean, server 13/14 suites green (226/227 tests) — 1 failing resume test is a test-mock gap, NOT a runtime bug (see M2 below)
- **Blockers:** RevenueCat not connected, no Apple Developer account, domain not purchased
- **Audit findings (2026-04-11):** 13 verified issues — 2 Critical, 6 High, 5 Medium. See `USER_TESTING_FINDINGS_2026-04-11.md` for details and `CLI_PROMPTS_TO_FIX_FINDINGS.md` for ready-to-paste CLI tasks (both in Winlet repo).

#### Winlet Pre-Beta Issue Todo (2026-04-11 audit)

**Critical — must fix before expanding beta beyond family cohort:**
- [ ] **C1** — Cost-guard check-then-act race (server/src/lib/cost-guard.ts:256-354) — same shape as Plainly H2, Vinla C3; needs atomic `UPDATE ... WHERE ... RETURNING`
- [ ] **C2** — Email webhook secret compared with non-timing-safe `!==` (server/src/routes/webhooks.ts:104) — use `crypto.timingSafeEqual`

**High — fix before app-store submission:**
- [ ] **H1** — Registration race between SELECT and INSERT (server/src/routes/auth.ts:71-80) — use `INSERT ON CONFLICT`
- [ ] **H2** — Login timing side channel reveals valid emails (server/src/routes/auth.ts:99-111) — run dummy bcrypt on unknown email
- [ ] **H3** — Chat stream doesn't abort on client disconnect (server/src/routes/chat.ts:146-172) — add `req.on('close', ...)` that calls `stream.controller.abort()`
- [ ] **H4** — Pro+ Sonnet 50/month cap defined but never enforced (cost-guard.ts:70 + chat.ts:21-24) — potential $72/mo AI cost vs $6.99 revenue per heavy Pro+ user
- [ ] **H5** — Cost guard fails OPEN to free tier on DB error (cost-guard.ts:240-246, 371-376) — fail closed with cached tier (same shape as Plainly H6)
- [ ] **H6** — `getUserTier` hardcoded to `pro_plus` for all users (cost-guard.ts:148-153) — documented in CLAUDE.md as pre-launch blocker; must ship paired with H4 or AI budget bleeds

**Medium — first post-beta sprint:**
- [ ] **M1** — Output guardrails log-only, never block (chat.ts:174-178) — add persistent telemetry table + alerting
- [ ] **M2** — resume.test.ts mock missing `costGuardIncrement` export (baseline test failure — test mock gap, not runtime bug; fix adds one line)
- [ ] **M3** — `/me` endpoint hardcodes `subscription_tier = 'pro_plus'` (auth.ts:195-197) — remove with H6 in same commit
- [ ] **M4** — Dynamic SQL in PATCH /me (auth.ts:202-217) — no injection today but fragile; switch to explicit allowlist
- [ ] **M5** — Cost guard daily reset uses UTC only (cost-guard.ts:252) — same shape as Plainly M4

**Verified NOT bugs (agents were wrong):** rate limiting IS present on /register, /login, /refresh (index.ts:107-118); JWT_SECRET length IS validated (middleware/auth.ts:8-10, unlike Plainly/Vinla); `personalization` and `memoryContext` ARE sanitized via `sanitizePromptInput` (system-prompt.ts:40-53); system prompt IS built server-side (not Vinla C1 shape); `getChatModel` IS tier-aware (chat.ts:21-24); crisis detection runs BEFORE Claude call; input guardrails check ALL user messages (multi-turn injection covered); `authStore.ts` JSON.parse IS wrapped in try/catch; `streaming.ts` JSON.parse IS wrapped; Slack HMAC IS timing-safe (lib/slack.ts); `costGuardIncrement` IS exported from cost-guard.ts:201; mobile app uses contexts/hooks (no Zustand) so Vinla M1 shape does not apply.

### Fraus (AI Scam Detector — Quick-Revenue Bet, 2026-04-17)
- **Target:** Boomers + older adults + adult children who worry about them
- **Model:** Family-pay ($9.99/mo for 5 seats) + individual ($4.99/mo) + free tier (5 checks/mo)
- **Core value:** Paste a text/email/voicemail → instant Safe/Suspicious/Scam verdict in plain English with red flags + next steps
- **Phase 1 shipped (2026-04-17):** Next.js 14 landing page + waitlist (Neon, auto-creating table) + Meta Pixel. Typecheck + build clean. Private GitHub repo. NOT deployed.
- **Phase 2 MVP (not started):** Mirror Winlet — Express + JWT + Claude (Haiku default, Sonnet for image/URL deep dives) + Expo mobile + RevenueCat
- **Strategy:** Validate-then-build. Green-light MVP only if Meta ad CPL < $3 on 55+ audience; reposition if CPL > $8.
- **Naming cleared 2026-04-17:** avoided "ScamShield" (Singapore GovTech + T-Mobile trademarks)
- **Blocked on owner:** Neon project, Meta Pixel, domain purchase (<your fraus domain>), USPTO intent-to-use ($350), first `npx vercel --prod`
- **Differentiators vs T-Mobile Scam Shield / Truecaller:** not a call-blocker; paste-any-message; family alerts; boomer-friendly UX; plain-English explanations
- See `jbrock1981/Scamly` (rename pending) repo: `TODO.md`, `CLAUDE.md`, `DEPLOY.md`

### Pillarly (Senior Medication Assistant — Quick-Revenue Bet, 2026-04-17)
- **Target:** Seniors (60+) managing multiple medications + their adult-child caregivers
- **Model:** Free (up to 3 meds) + Pro $7.99/mo (unlimited + voice + full interactions) + Family Pro+ $14.99/mo (5 members + missed-dose alerts)
- **Core value:** Point phone at pill bottle → OCR + plain-English explanation + reminders + interaction/allergy checks; family dashboard for adult children
- **Phase 1 shipped (2026-04-17):** Next.js 14 landing page + waitlist + Meta Pixel. Senior-friendly defaults (18px base, 1.6 line-height, big buttons). Disclaimer "assistant, not a medical device." Typecheck + build clean. Private GitHub repo. NOT deployed.
- **Phase 2 MVP (not started):** Mirror Winlet — Express + JWT + Claude Vision for OCR + RxNorm (free NIH) / DrugBank (paid) for interactions + Expo mobile (voice-first)
- **Strategy:** Validate-then-build. Green-light MVP only if Meta ad CPL < $4; reposition if CPL > $10.
- **Naming cleared 2026-04-17:** avoided "Pill Buddy" (multiple iOS conflicts) and "Dosely" (Skidoosh Games LLC)
- **Blocked on owner:** Neon project, Meta Pixel, domain purchase (pillarly.com/.app), USPTO intent-to-use ($350), first `npx vercel --prod`
- **Legal pre-launch gates (HARD BLOCKERS):** HIPAA review before shipping family tier (covered-entity risk); Apple medical-app guideline review (app must never recommend dosages); interaction output must never say "safe to take" — always defer to pharmacist
- **Differentiators vs Medisafe / MyTherapy / Pill Buddy:** OCR-first capture (not manual entry); voice-first; adult-child family dashboard with alerts; plain-English explanations via Claude
- See `jbrock1981/Pillarly` repo: `TODO.md`, `CLAUDE.md`, `DEPLOY.md`

### Tradingly (Day Trade Screener / FastAPI + Next.js — NOT Plainly Digital LLC; tracked here because audit was part of the same 2026-04-11 portfolio sweep)
- FastAPI backend on Render (512MB), Next.js frontend on Vercel
- Neon Postgres for auth, SQLite for ephemeral/paper-trading data
- Finnhub WebSocket → SSE real-time prices
- Sage AI scoring engine (Claude Haiku 4.5), paper trading, smart alerts, multi-timeframe analysis
- Tier model: Free / Pro / Pro Max
- Deployed to production via Render + Vercel
- **Baseline health (2026-04-11):** All 11 previously-truncated files restored (commit 91a17c5). Core auth/database layers sound. No test suite — manual verification only.
- **Audit findings (2026-04-11):** 24 verified issues — 4 Critical, 8 High, 9 Medium, 3 Low. See `AUDIT_FINDINGS_2026_04_11.md` for details and `CLI_PROMPTS_WAVE_1_CRITICAL.md` + `CLI_PROMPTS_WAVES_2_6.md` for ready-to-paste CLI tasks (both in DayTradeScreener repo).

#### Tradingly Production Issue Todo (2026-04-11 audit)

**Critical — user-visible today, fix before next deploy:**
- [ ] **C1** — `update_position` and `close_position` write to nonexistent columns (main.py:1067-1102) — crashes every position update/close with sqlite3.OperationalError. `user_positions` schema in database.py:77-86 lacks stop_loss, take_profit, exit_price, closed_at.
- [ ] **C2** — `DAILY_LIMITS = {"free": 0, "pro": 0, "pro_max": 100}` (ai_usage.py:15) — logic in check_ai_limit() blocks Pro tier users with 429 before any Claude call. Paying Pro users cannot use AI features. Free is correctly 403'd; Pro Max is the only working tier.
- [ ] **C3** — Stripe checkout creates duplicate customers on every purchase (payments.py:72) — `user.get("stripe_customer_id")` always None because get_user_by_id returns `_SAFE_USER_COLS` that excludes it. Stripe dashboard fills with orphan customers; billing history splits across IDs.
- [ ] **C4** — `customer.subscription.deleted` webhook queries SQLite (payments.py:117-130) but users live in Neon Postgres — cancellation never downgrades tier; canceled users keep Pro Max forever.

**High — pre-public-signup security + correctness:**
- [ ] **H1** — Refresh token stored in localStorage (frontend/src/lib/auth.ts:24-27) — XSS → 7-day account takeover path, compounded by H5 CSP unsafe-eval
- [ ] **H2** — `/api/auth/logout` endpoint does not exist; frontend calls it anyway and swallows the 404 (auth.ts:76-85). Tokens never added to blocklist; leaked tokens stay valid until natural expiry
- [ ] **H3** — In-memory `_blocklist` and `_login_attempts` (auth.py:47,50) — both lost on every Render redeploy; lockout resets enable unlimited brute-force via redeploy trigger; behind N instances threshold becomes 5×N
- [ ] **H4** — Register SELECT-then-INSERT race (auth.py:239-244) — concurrent registrations with same email both pass pre-check, second INSERT raises raw asyncpg/sqlite exception instead of clean 409; bcrypt DoS amplifier
- [ ] **H5** — CSP allows `'unsafe-inline'` AND `'unsafe-eval'` in script-src (main.py:160-168) — effectively disables XSS protection. TODO.md tracks style-src only, not script-src
- [ ] **H6** — Request body size limit bypass (main.py:177-189) — chunked-encoding requests omit Content-Length and sail through; attacker can upload 500MB JSON before FastAPI parses
- [ ] **H7** — Sage AI trade advice has no output guardrails for financial-advice liability (ai_sage.py:77-82) — "Give a 2-3 sentence actionable take for a day trader. Be direct." with no disclaimer, no output-side check, user-provided `news_summary` concatenated raw into Claude prompt (prompt injection vector for retail-facing financial product)
- [ ] **H8** — `ai_earnings_summary` has no auth or cost guard (ai_sage.py:140-164) — no user_id, no check_ai_limit, no record_ai_call; transcript_text[:3000] injected directly into prompt (second prompt injection vector); 5-min cache is only mitigation

**Medium — first post-production sprint:**
- [ ] **M1** — 5 modules (alert_chains, earnings_intel, monte_carlo, replay, trade_grading) import `get_usage` which does not exist (middleware.py:4, database.py lacks it); they crash on import; none are mounted in main.py, so the app boots, but tier gating in those modules is silently skipped
- [ ] **M2** — [verified NOT a bug: _record_login_attempt ordering is intentional; bcrypt is skipped on unknown email via short-circuit; flagged by agent but correct]
- [ ] **M3** — `increment_usage` INSERT then SELECT race on Postgres branch (database.py:343-352) — two statements, use `RETURNING screen_count` for atomic read
- [ ] **M4** — EventSource reconnect closure-capture race (frontend/src/lib/realtime.ts:65-83) — narrow window where onerror setTimeout survives effect cleanup and opens stale EventSource for old symbols
- [ ] **M5** — No root-level ErrorBoundary (layout.tsx) — only the dashboard page is wrapped (page.tsx:389-589); login/register/forgot-password render white Next.js error screen on crash
- [ ] **M6** — iOS PWA home-screen title still `"DTS"` (layout.tsx:20) — metadata.title correctly says "Tradingly" but appleWebApp.title is stale
- [ ] **M7** — `api_v1.v1_screen` silent error suppression (api_v1.py:100-101) — `except Exception: row["signal"] = "ERROR"` with no logging; hardest-to-debug pattern in production
- [ ] **M8** — `stream_prices` returns dict instead of raising on Finnhub not configured (stream.py:33-34) — FastAPI serializes as 200 JSON; EventSource sees success and never reconnects cleanly
- [ ] **M9** — Logout only clears `dts-access-token` and `dts-refresh-token` (auth.ts:29-32) — watchlists, positions (SageAdvisor.tsx:209 POSITIONS_KEY), preferences stay in localStorage; shared-computer privacy leak

**Low — backlog:**
- [ ] **L1** — `X-XSS-Protection: 1; mode=block` header (main.py:156) — deprecated, ignored by modern browsers, can enable reflected-XSS in legacy IE
- [ ] **L2** — `JWT_SECRET` fallback "dts-dev-secret-local-only" gated only on `ENV == "production"` (auth.py:35-39) — Render sets `RENDER=true` not `ENV`; production deploy without JWT_SECRET silently uses hardcoded dev secret
- [ ] **L3** — `ALLOWED_EMAILS` hardcoded in source (auth.py:27-33) — already on TODO.md

**Verified NOT bugs (agents were wrong):** SSE stream IS aborting on client disconnect (stream.py:47 checks request.is_disconnected() inside the loop); CORS is NOT open — allow_origins is a specific list plus a scoped Vercel regex, allow_credentials=False (main.py:141-148); DAILY_LIMITS is NOT an unbounded-cost exposure — the actual bug (C2) is the opposite, Pro is blocked entirely; `_record_login_attempt` ordering around bcrypt IS correct (short-circuit on unknown email); EventSource reconnect is NOT an unbounded memory leak — useEffect cleanup does fire and clearTimeout runs, the real bug (M4) is a narrow race.

---

## Cross-Product Action Items

### Immediate
- [ ] Apple Developer account ($99/yr) — needed for all 4 core apps + future Fraus/Pillarly MVPs
- [ ] RevenueCat integration — needed for all apps with paid tiers
- [ ] Register Notch DBA under Plainly Digital LLC
- [ ] Deploy Fraus landing page (Neon + Vercel + Meta Pixel) — quick-revenue validation gate
- [ ] Deploy Pillarly landing page (Neon + Vercel + Meta Pixel) — quick-revenue validation gate
- [ ] USPTO intent-to-use filings for Fraus + Pillarly ($350 each) before public ad spend

### Short-Term
- [ ] Configure Plainly server env vars on Render (Plaid, Google OAuth, internal API key)
- [ ] Notch Privacy Policy + Terms of Service
- [ ] Vinla: Supabase data sync + RLS policies
- [ ] Public beta launches: Plainly, Vinla
- [ ] Fraus + Pillarly $50/48hr Meta ad validation runs — decide MVP green-light

### Medium-Term
- [ ] App Store submissions (all apps need eas.json credentials)
- [ ] Winlet domain purchase (<your winlet domain>)
- [ ] Fraus + Pillarly domain purchases (contingent on ad validation)
- [ ] Marketing / ASO strategy
- [ ] Pillarly HIPAA review + Apple medical-app guideline review (HARD gates for MVP launch)

---

## Other Entities (NOT in this repo)

| Entity | Repo | Owner | Relationship |
|--------|------|-------|-------------|
| Advisedly Compliance LLC | jbrock1981/Advisedly | Jonathan Brock | Separate standalone LLC — v1.0 cut-ready (offline license enforcement H1 + Helm chart H2 shipped 2026-04-14, commits 5789140 + 892f491). TRL 7, SAM.gov registered (UEI: XSZ6TYQM2F54). DLA CAGE review in progress (responded 2026-04-14). Tradewinds Solutions Marketplace video submission compliance-cleared 2026-04-14, in queue for scheduled assessment (NTE $1.7M Prototype OTA path). 4 V1-READINESS docs complete: licensing/deploy design, feature inventory (135 features / 1,624 endpoints), automation inventory (68 automations), competitive analysis Q2-2026. AF demo prep pending. |
| CastFreely LLC (not formed) | jbrock1981/CastFreely | Lauri Brock | Separate entity |

See each entity's own repo for their master tracker.

---

## Legal Documents (in `legal/`)

- LLC Operating Agreement (v3)
- IP Assignment Agreement
- NDA template
- Plainly Terms of Service
- Vinla Terms of Service
- Plainly Privacy Policy
- Vinla Privacy Policy

### Missing Legal
- [ ] Notch Terms of Service
- [ ] Notch Privacy Policy
- [ ] Winlet Terms of Service
- [ ] Winlet Privacy Policy
- [ ] Fraus Terms of Service (landing page currently has no legal pages)
- [ ] Fraus Privacy Policy (forwarded scam content may contain third-party PII — needs counsel)
- [ ] Pillarly Terms of Service (MUST include "not a medical device" + "not medical advice" carve-outs)
- [ ] Pillarly Privacy Policy (medication names + schedules are sensitive health info)
- [ ] Pillarly HIPAA review (family sharing creates covered-entity risk surface)
