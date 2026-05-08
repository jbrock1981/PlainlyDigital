# Plainly Digital LLC — Master Tracker

**Last Updated:** April 4, 2026 (late night — all truncations resolved, Tradingly rebranded + optimized, Vytally user tested)
**Parent Entity:** Plainly Digital LLC (Tennessee, manager-managed, EIN: 41-4877857, SOS #002094776)
**Owner:** Jonathan Brock
**Address:** 1309 Case Rd, Prospect, TN 38477
- Class A (Founder) / Class B (Partner) membership structure
- Successor Managing Member: Wife designated
- Revocable living trust recommended but not yet established
- FinCEN BOI report: No longer required as of 2026

**Note:** Advisedly Compliance LLC has its own separate master tracker in the Advisedly repo (docs/master-tracker.md).

---

## ENTITIES & REPOS

| Entity | Type | Status | Repo | Local Path |
|--------|------|--------|------|-----------|
| Plainly | DBA under Plainly Digital | ~95%, pre-beta | jbrock1981/Plainly | C:\Users\jbroc\Plainly |
| Vytally | DBA under Plainly Digital | ~70%, family beta | jbrock1981/vytally | C:\Users\jbroc\vytally |
| 42ly | DBA under Plainly Digital (DBA NOT REGISTERED) | Waves 0-8 complete, deployed | jbrock1981/42ly | C:\Users\jbroc\42ly |
| Accomplishly | Under Plainly Digital | All 4 phases, deployed & live | jbrock1981/Accomplishly | C:\Users\jbroc\Accomplishly |
| Tradingly | Under Plainly Digital | Deployed, 37+ endpoints, rebranded, perf optimized | jbrock1981/DayTradeScreener | C:\Users\jbroc\DayTradeScreener |
| CastFreely | Separate entity (LLC NOT YET FORMED) | ~75-80%, all 9 waves, 423 tests | jbrock1981/CastFreely | C:\Users\jbroc\CastFreely |
| Fraus | Under Plainly Digital | Phase 1 landing scaffold only (2026-04-17), not deployed | jbrock1981/Scamly (private; rename pending) | C:\Users\jbroc\Scamly |
| Pillarly | Under Plainly Digital | Phase 1 landing scaffold only (2026-04-17), not deployed | jbrock1981/Pillarly (private) | C:\Users\jbroc\Pillarly |

> **Note (2026-04-17):** This document is the older detailed tracker. The actively maintained master is `../Plainly_Digital_Master_Tracker.md` at the repo root. See that doc for full Fraus + Pillarly details, quick-revenue validation strategy (landing-page ads → MVP green-light thresholds), and updated Cross-Product Action Items.

---

## PLAINLY — Financial Literacy App

### Dev Status: ~95% COMPLETE — Pre-beta (Render build broken — 7 truncated files from CLI)

**Deployed:** plainly-psi.vercel.app (web), plainly-c8jw.onrender.com (API), Neon (DB)
**Stack:** Expo RN + Express + Neon PostgreSQL + Claude AI
**Target:** Ages 18-28 | 18 modules, 121 lessons, ~240 quizzes | Claude AI coach "Sage"
**Tests:** 493+ Jest tests passing (24+ test suites)
**Routes:** 19 server route files | **Hooks:** 11 frontend hooks | **Components:** 18

**What's built:**
- Full auth (email/password + Google OAuth + Apple Sign-In)
- 18 modules, 121 lessons, ~240 quiz cards
- AI Coach "Sage" (streaming Claude Sonnet 4.6, personality, follow-up chips, lesson nudges, voice input/output)
- Voice coaching: Whisper API STT, expo-speech TTS, full voice conversation mode
- 5 interactive calculators (compound interest, debt payoff, emergency fund, 50/30/20, rent)
- "What If" spending simulation engine (7 scenario types, Plaid-powered)
- Money IQ assessment, Money Personality AI profile, Money Roast, Future You Visualizer
- Daily content system (60+ facts, 30 quizzes, 12 seasonal alerts, daily challenges)
- AI-personalized micro-content feed (Claude Haiku, 5 card types, 12hr cache)
- "Your Week in Money" AI-generated weekly summary cards
- Push notifications, real-time spending alerts (Plaid webhook → pattern detection → push)
- Embedded finance / affiliate system (11 curated products, Sage-aware, disclosure on every card)
- Certification: "Plainly Certified — Personal Finance Foundations" (50-question bank, verifiable credential)
- Free/Pro/Pro+ monetization ($0/$2.99/$6.99)
- Plaid Link SDK + AES-256-GCM token encryption
- Internationalization (EN/ES), anti-gamification, UX polish
- AI Cost Guard (all endpoints), Sage 3-Layer Architecture, NIST AI RMF governance
- Financial health score (0-100), Salary Explorer with negotiation practice
- 15 money scenarios, goal tracking with templates
- **NEW (April 3-4):** Bank statement ingestion (PDF/CSV/Excel upload, multer, AI categorization)
- **NEW:** Spending Trends (monthly breakdowns, category insights, AI analysis)
- **NEW:** Budgets (create, track vs actuals, AI auto-generate via 50/30/20)
- **NEW:** Subscription detection (recurring charge identification, Sage evaluation)
- **NEW:** Credit Score tracking (with AI tips)
- **NEW:** Income Tracker (payroll vs freelance, 6-month trends)
- **NEW:** Side Hustle ROI calculator
- **NEW:** Negotiate Bills (AI-powered negotiation scripts)
- **NEW:** Spending Challenges
- **NEW:** Parent/Guardian access screen
- **NEW:** "How Plainly Makes Money" transparency page

**Tools page sections (verified April 4 user test):**
- CALCULATORS: Compound Interest, Debt Payoff, Emergency Fund, 50/30/20, What Can I Afford?, Rent Affordability
- YOUR MONEY: Spending Trends, Budgets, Subscriptions, Credit Score, Income Tracker, Side Hustle ROI
- PLANNING: What If?, Financial Goals, Salary Explorer
- INTERACTIVE: Negotiate Bills, Money Scenarios, Quick Tips Feed
- RECOMMENDED: Affiliate product recommendations with disclosure

**User Test Results (April 4, Cowork browser):**
- Home: Personalized greeting, life moment card, stats, daily quiz, seasonal tip — all working
- Learn: 18 modules/121 lessons loading, lesson viewer with card UI and progress bar — working
- Tools: All calculators functional (compound interest live-calculating), new money tools visible — working
- Coach: Sage responding with streaming, follow-up chips, AI badge, speaker/bookmark icons — working
- Profile: Progress stats, milestones, Money Personality, settings, account management — working
- Issues found:
  - Coach markdown not rendering (raw `**bold**` showing instead of bold text) — react-markdown may not be wired for coach bubbles
  - Follow-up chips after budget question show debt-related topics instead of budget-related — chip generation needs context fix
  - Text input on web doesn't accept browser typing (React Native TextInput limitation on web) — suggested question chips work as workaround

**Render Build Status (April 4):**
Previously broken by 20+ truncated files across multiple CLI sessions. All truncated files now restored from git history (commits f41b281, 0f26f5b, bd6472f). Key fixes applied:
- All 20+ server files restored to complete state from security hardening commit (544b81d)
- Cost guard fail-closed (catch block returns `allowed: false`)
- Cross-platform storage: all AsyncStorage replaced with platform-aware helpers (getItem/setItem/removeItem/getAllKeys/multiGet)
- @types/multer moved to production dependencies
- server/tsconfig.json excludes __tests__
- **Needs push from local terminal** (`git push origin main`) to trigger Render rebuild

**Remaining P0 (before beta):**
- [x] ~~Fix 20+ truncated files~~ → ALL RESTORED (commits f41b281, 0f26f5b, bd6472f)
- [x] ~~Replace AsyncStorage with platform-aware storage~~ → ALL 17 files migrated (commit bd6472f)
- [ ] **Push to remote** (`git push origin main` from local terminal — triggers Render rebuild)
- [ ] Configure remaining Render env vars (PLAID_CLIENT_ID, PLAID_SECRET, GOOGLE_CLIENT_ID, INTERNAL_API_KEY)
- [ ] Run 002_add_transactions.sql + 006_fix_user_usage.sql migrations on Neon
- [ ] End-to-end smoke test on device
- [ ] Fill eas.json app store credentials
- [ ] Integrate RevenueCat SDK for real payment processing

**Remaining P1/P2:**
- [ ] Fix coach markdown rendering (wire react-markdown for chat bubbles)
- [ ] Fix follow-up chip context (chips should match conversation topic)
- [ ] Plaid production access (apply 1-2 weeks before launch)
- [ ] Short-form video on lesson hooks
- [ ] Pro+ tier with Sonnet-powered Sage

---

## VYTALLY — Personal Health Intelligence App

### Dev Status: ~70% COMPLETE — Family beta | All truncations fixed, 290 tests passing

**Deployed:** health-ai-jbrock1981s-projects.vercel.app (web) | Expo (mobile buildable)
**Stack:** Expo RN + Supabase + Claude AI
**Target:** Ages 18-28 | Free / $2.99 Pro / $6.99 Pro+
**Supabase:** ohnoaetkvkevkvrdpwmp.supabase.co
**Status:** Private family beta — daughter actively testing
**Tests:** 290 Jest tests passing (14 test suites)
**User Test (April 4):** All 5 tabs verified working — Dashboard, Log, Sage AI coach, Community, More

**What's built (Waves 0-7 + security hardening):**
- Dashboard with Bloom garden, streak badge, daily checklist, signals carousel
- Multi-type logging (food, water, sleep, mood/energy/stress/anxiety/gratitude, exercise)
- 4 food input methods: manual + barcode (Open Food Facts) + photo (Claude Vision) + conversational AI
- Deep nutrient tracking (USDA FoodData Central, 29 nutrients, RDA dashboard)
- AI Coach "Sage" (streaming Sonnet 4.6, 30-day context, mood-adaptive)
- 2-layer crisis detection (hardened against Unicode/homoglyph/l33tspeak)
- Input/output guardrails, prompt sanitization, per-user AI cost guard (fail-closed)
- Auth improvements, Supabase migration, Free/Pro/Pro+ gating
- Cross-domain intelligence engine, PHQ-2/GAD-2 screening, Gentle Mode
- Bloom virtual wellness garden, Apple Health / Health Connect
- Push notifications, subscription system, privacy/consent flow
- Sage 3-Layer Architecture + NIST AI RMF governance
- **NEW (April 4):** Security hardening — rate limiting, security headers, input validation

**CLI Truncation Damage: RESOLVED** (commit f06c5aa restored all 7 files from git history)
All auth endpoints, AI services, DB init, and package.json restored and verified. 290 tests passing. 0 TypeScript errors.

**Phase 0 — Pre-Launch Blockers:**
- [ ] Server-side PostgreSQL (Supabase) — data still in local SQLite
- [ ] Data sync (local SQLite ↔ Supabase cloud)
- [ ] Row-level security + Supabase user_usage table
- [ ] Encryption at rest + backup/DR + audit logging
- [ ] AI medical disclaimer in chat UI
- [ ] Age gate (18+ or 13+ with parental consent)
- [ ] Insurance (GL + Cyber + E&O)
- [ ] Rename Vercel project health-ai → vytally
- [ ] Fill eas.json, RevenueCat integration

**Key threat:** Apple Health+ launching mid-late 2026 — must establish users first.

---

## 42ly — AI Life Advisor App

### Dev Status: ALL WAVES COMPLETE (0-8) — 718 tests, deployed

**Deployed:** 42ly.vercel.app | 42ly-api.vercel.app
**Stack:** React Native/Expo 55 + Express + Supabase + Claude AI
**Target:** Gen Z (16-27), "Sage" AI life advisor
**Supabase:** vyparqcxakpzddmrjyin (us-east-1)
**Tests:** 718 tests passing (318 app + 400 server, 61 test files)

**What's built (Waves 0-8):**
- Streaming chat UI with Claude AI "Sage" (toughest variant: "tough love dad energy")
- Express API on Vercel, Supabase auth with email allowlist gate
- 14 tables with RLS + 3 migrations
- Journal (mood, AI reflections, cross-entry patterns, life review reports)
- Goals (CRUD, categories, milestones, AI-suggested)
- Crisis detection (two-layer, 55+ patterns, hardened) + 988/741741 warm handoff
- Life Domain Dashboard ("The 42 Map"): 6 domains, radar chart, health scoring
- Decision Engine ("42 Framework"): weighted pros/cons, scenario modeling
- Persistent Memory & Growth Tracking, Action Quests
- Career Command Center, Money Basics ("The 42 Money Plan")
- Relationship Intelligence with abuse/violence detection + DV hotline
- Weekly Life Review, Voice Mode, Share-Worthy Insights
- Personality Calibration ("Train the AI": 12-question bank)
- Monetization Infrastructure, Multi-Language (EN/ES)
- Ecosystem Integration (Vytally/Plainly sync), Year in Review
- NIST AI RMF governance, Sage 3-Layer Architecture
- Server hardening: JWT, 3-tier rate limiting, cost-guard, CORS, 50KB limit

**What's NOT built yet:**
- [ ] Parental controls enforcement
- [ ] Privacy Policy + Terms of Service
- [ ] Register 42ly DBA under Plainly Digital LLC
- [ ] USPTO trademark check + filing
- [ ] Google OAuth provider config in Supabase
- [ ] eas.json credentials, RevenueCat integration
- [ ] App Store/Play Store submission

---

## ACCOMPLISHLY — Personal Wins Tracker

### Dev Status: ALL 4 PHASES COMPLETE — 379 tests, deployed & live | All truncations fixed

**Deployed:** API: accomplishly-api.onrender.com | Web: web-two-lac-36.vercel.app
**Stack:** React Native (Expo SDK 53) + Express/Node + Neon PostgreSQL + Claude API
**Target:** Adults — self-doubt, imposter syndrome, career transitions, caregivers
**Database:** Neon (project: accomplishly, 13 tables, 14 indexes)
**Tests:** 379 passing (204 server + 125 mobile + 25 web + 25 cost guard)

**Core concept:** Backward-looking accomplishments app. Not goals or habits — things you did that mattered. Cumulative, never punitive. No streaks, no guilt.

**What's built:**
- Full auth, Wins CRUD + "Lift Me Up" random retrieval + cumulative stats
- Log Win modal with celebration animation, photo attachments, voice capture
- Calendar heatmap (GitHub-style), AI pattern insights + Sage AI chat with crisis detection
- Proof folder, Life Resume & Year in Review, shareable win cards (4 templates)
- Dark mode (WCAG AA), push notifications, team/family spaces, web companion
- Integrations (Slack, email, calendar), GDPR export, account deletion
- AI Cost Guard (centralized), Sage 3-Layer (warmest variant), NIST AI RMF
- **NEW (April 4):** Security hardening (SAST/DAST/STIG), Send Hype UI, circle streaks, Wrapped share, NIST governance docs, legal docs (Privacy Policy + ToS), hype_drops table, 6 market-disrupting features (Wrapped, Screenshot Dump, Hype Circle, etc.)

**CLI Truncation Damage: RESOLVED** (commit b648bf9 restored space-detail.tsx and spaces.tsx from git history)
server/src/index.ts, log-win.tsx, and onboarding.tsx were already complete. TypeScript compiles with 0 errors in both server and app.

**What's NOT built yet:**
- [ ] RevenueCat IAP integration
- [ ] Google OAuth client ID
- [ ] Apple Developer account ($99/yr — shared)
- [ ] Domain + trademark

**Monetization:** Free / Pro $2.99 / Pro+ $6.99 + boost packs. No ads ever. Lift Me Up always free.

---

## TRADINGLY — AI-Powered Day Trading Screener

### Dev Status: DEPLOYED — 37+ endpoints, Sage AI scoring, Finnhub real-time | All truncations fixed, rebranded, performance optimized

**Domain:** tradingly.app (purchasing via GoDaddy)
**Live Frontend:** frontend-iota-livid-71.vercel.app → tradingly.app (Vercel, rename pending)
**Live API:** daytrade-screener-api.onrender.com → tradingly-api.onrender.com (Render, rename pending)
**Stack:** Next.js 15 (React 19) + FastAPI (Python 3.12) + Finnhub WebSocket + Neon Postgres + SQLite + Stripe + Alpaca
**Tests:** 34 tests (94.1%), 16/16 endpoints tested
**Backend files:** 476 Python modules | **Frontend:** 84 components
**Rebrand commit:** `1d72df4` — display names, meta tags, manifest, legal docs, render.yaml, CORS, package.json all updated. localStorage keys kept as `dts-` for backward compat.

**What's built:**
- **Sage AI Trading Assistant:** Sage Score (0-100, A+ to D), multi-factor confluence scoring
- Signal narration (plain-English trade thesis), risk guardrails, What-If scenarios
- Live Signal Dashboard (auto-refreshing Buy/Sell scanning ~540 tickers)
- 9 technical indicators: VWAP, RSI, MACD, Bollinger, EMA 9/21, ATR, RVOL, Stochastic RSI, OBV
- 6 strategy presets (Gap & Go, VWAP Bounce, Momentum Breakout, etc.)
- Natural language queries, customizable dashboard layout
- TradingView Lightweight Charts with drawing tools (trendlines, Fibonacci, rectangles)
- Volume profile with POC, multi-panel crosshair sync
- 200+ term financial sentiment lexicon
- Optional Claude API for enhanced analysis + AI morning briefing
- **Finnhub WebSocket real-time streaming** (replaced Polygon.io): in-memory price cache, trade tape (last 50/symbol), simulated order book from trade clustering, SSE bridge to frontend (0.5s poll, 30s heartbeat)
- **Paper trading now SQLite-backed** (aiosqlite, async, user-scoped via JWT — survives restarts)
- **Hybrid DB:** Neon Postgres (auth, preferences, usage) + SQLite (paper trading, alerts, ephemeral data)
- Alpaca broker integration (paper & live)
- Position calculator (Kelly Criterion), trade journal
- Options: GEX analysis, unusual flow scanner, multi-leg strategy builder
- JWT auth (local + Neon Postgres) + Stripe subscription (Free/Pro/Pro Max)
- Invite-only whitelist (5 emails)
- **NEW (April 4):** Phase 9 — AI Sage integration, advanced math, trader workflow, legal infrastructure. Rebrand DayTradeScreener → Tradingly complete.
- **NEW (April 4 late):** Performance optimization — React.memo on TickerTable rows, 4 custom hooks extracted from page.tsx (useScreenerState, useChartState, useAuthState, useAutoRefresh), 200ms debounced ticker search with useMemo. 0 new TS errors.

**CLI Truncation Damage: RESOLVED**
- Backend: All 9 Python files restored (commit 91a17c5). All 71 Python files parse clean.
- Frontend: page.tsx rewritten with custom hooks (commit 681834e). layout.tsx clean.
- Rebrand: All user-facing strings changed DayTradeScreener → Tradingly (commit a781241, 9 files, 12 replacements).

**Remaining:**

Critical:
- [ ] Fix ticker click detail view (fails silently)
- [ ] Fix backend cold starts (Render free tier — upgrade to paid $7/mo)
- [ ] Fix NO_DATA failure rate on some tickers
- [x] ~~Persist paper trading~~ → DONE (SQLite-backed, async)
- [x] ~~Upgrade to real-time data~~ → DONE (Finnhub WebSocket replaces Polygon.io)

High:
- [ ] Cache-busting for Vercel deployments
- [ ] Loading states/skeletons for all API calls
- [x] ~~WebSocket streaming~~ → DONE (Finnhub WS → price cache → SSE)
- [ ] Data quality monitoring (/api/health/data endpoint)

Medium/Legal:
- [ ] Pre-market / after-hours data display
- [ ] Expand beyond S&P 500 (Russell 2000, ETFs, user customs)
- [ ] Mobile-responsive optimization
- [ ] Terms of Service + Privacy Policy + SEC/FINRA disclaimers
- [ ] Clean up legacy Polygon.io references (backward-compat aliases in realtime.py, .env.example)

**Rebrand remaining (April 3):**
- [ ] Vercel: rename project "frontend" → "tradingly", connect tradingly.app domain
- [ ] Render: rename service "daytrade-screener-api" → "tradingly-api", update ALLOWED_ORIGINS
- [ ] Vercel env: update NEXT_PUBLIC_API_URL → https://tradingly-api.onrender.com
- [ ] GitHub: rename repo jbrock1981/DayTradeScreener → jbrock1981/Tradingly
- [ ] Update README.md (still shows "DayTrade Screener" on line 1)
- [ ] Trademark search + filing for "Tradingly" (~$350)

**Pricing:** Free / Pro / Pro Max (via Stripe)

---

## CASTFREELY — Casting, Scheduling & Payment Platform

### Dev Status: ~75-80% COMPLETE — Feature complete, all 9 waves done

**Deployed:** castfreely.com (Vercel, SSL active)
**Entity:** CastFreely LLC (Tennessee — NOT YET FORMED, Lauri Brock founder)
**Stack:** Next.js 16 (App Router, React 19) + TypeScript + Tailwind + shadcn/ui + Supabase Auth + Neon PostgreSQL + Claude API
**Tests:** 423 passing
**Endpoints:** 37 API routes | **Pages:** 20 | **DB:** 23 tables, 11 indexes

**What's built (Waves 1-9):**
- Full auth (Supabase, gated to 2 emails during testing)
- Actor/CD/Production dashboards with role-specific features
- Submissions flow, gated messaging with content safety (blocks phone/email/SSN/social)
- Scheduling system, digital vouchers (replaces paper SAG/non-union vouchers)
- Contracts system, production portal
- AI Intelligence Layer (16 Claude-powered features): profile optimizer, role match, audition prep, breakdown writer, submission screener, compliance monitor
- Safety & Inclusion: production reputation system, safety reporting, SAG tracker, Wall of Shame/Fame transparency
- Ecosystem: agent roster tiers, Founder's Circle "Big 50", referral engine, bulk submission API, verified talent API, audition rooms
- RABS groundwork, SEO content pages, full E2E test suite
- OWASP audit passed, 0 critical/high CVEs
- Zod validation, React Hook Form, accessibility

**What's NOT built / blockers:**
- [ ] CastFreely LLC formation ($300 TN filing) + EIN + bank account
- [ ] SAG-AFTRA legal review (CRITICAL — required before any payment code)
- [ ] Stripe Connect integration (Phase 2+, blocked on legal review)
- [ ] Terms of Service + Privacy Policy + Operating Agreement
- [ ] Insurance (GL, Cyber, E&O)
- [ ] Trademark (~$350/class), branding refinement
- [ ] Real-time messaging (Supabase Realtime or Ably — Phase 4+)
- [ ] Background jobs (Inngest/Trigger.dev — Phase 3+)
- [ ] Open auth to public (currently gated to 2 test emails)

---

## LEGAL DOCUMENTS INVENTORY

### Plainly Digital LLC (Claude- repo legal/)
| Doc | Status |
|-----|--------|
| Operating Agreement (v1, v2, v3) | Exists, needs attorney review |
| IP Assignment Agreement | Exists |
| NDA | Exists |
| Plainly Terms of Service + Privacy Policy | Exists, needs review |
| Vytally Terms of Service + Privacy Policy | Exists, needs review |

### Still needed:
- [ ] 42ly Terms of Service + Privacy Policy
- [ ] Accomplishly Terms of Service + Privacy Policy
- [ ] Tradingly Terms of Service + Privacy Policy
- [ ] CastFreely Terms of Service + Privacy Policy + Operating Agreement (Lauri Brock)
- [ ] All docs need attorney review before commercial use

---

## SAGE 3-LAYER ARCHITECTURE (Cross-Portfolio)

All consumer apps share the Sage AI personality system:

**Layer 1 — Brand Personality (identical across all apps):** Direct, warm but not soft, practical, no judgment, humor as tool. 8th-grade reading level, casual tone, under 200 words, 4-part structure (direct answer → why → applied to user → one next action).

**Layer 2 — Domain Expertise (unique per app):**
- **42ly:** Life advisor — most direct ("tough love dad energy")
- **Vytally:** Health coach — direct but health-sensitive, mood-adaptive, eating disorder aware
- **Plainly:** Financial coach — warm older-sibling energy, makes money approachable
- **Accomplishly:** Self-worth coach — warmest variant, celebration-focused, validation-first
- **Tradingly:** Trading assistant — data-driven, risk-aware, confidence-graded (A+ to D)

**Layer 3 — User Personalization (per user, per app):** Unique context injection (onboarding, usage patterns, domain-specific signals). 42ly Layer 3 intentionally NOT shared with other apps (regulatory/bias risk, NIST AI RMF MAP 2.3).

---

## MONETIZATION STRATEGY — Consumer Apps

**Philosophy:** Price so low it never feels like a barrier. No ads, ever. Crisis/safety features always free.

**Payment Processor:** RevenueCat (wraps Apple/Google IAP + Stripe for web). Free until $2.5K MRR.
**Free Trials:** 7 days on all paid tiers. **Annual Discount:** 2 months free (~17% off).
**Boost Packs:** $1.99 (+50 AI calls) or $4.99 (+200 AI calls) — impulse-priced.

### Standardized 3-Tier Pricing
| Tier | Monthly | Annual | AI Model | Key Unlocks |
|------|---------|--------|----------|-------------|
| **Free** | $0 | $0 | Haiku 4.5 | Core features, education, crisis — always free |
| **Pro** | $2.99/mo | $24.99/yr | Haiku 4.5 | Full AI coaching, advanced features, exports |
| **Pro+** | $6.99/mo | $57.99/yr | Sonnet 4.6 | Premium AI, all features, priority responses |

### Tradingly (Separate)
Free / Pro / Pro Max (via Stripe) — pricing TBD

**Projected at 20K users (consumer apps):** ~$10,500/mo (~$9,300-9,700 net)

---

## COMPLETION SUMMARY

| Product | Dev % | Tests | Status | Biggest Blocker |
|---------|-------|-------|--------|-----------------|
| **Plainly** | ~95% | 493+ | Truncations fixed, AsyncStorage migrated, needs push+rebuild | Push to remote, Render env vars, eas.json, RevenueCat |
| **Vytally** | ~70% | 290 | All truncations fixed, 290 tests passing, user tested (all 5 tabs working) | SQLite→Supabase migration, age gate, insurance |
| **42ly** | Waves 0-8 | 718 | All complete, deployed, invite-only | Privacy Policy/ToS, DBA, RevenueCat |
| **Accomplishly** | All 4 phases | 379 | All truncations fixed, 0 TS errors, deployed | RevenueCat, Apple Dev account, domain |
| **Tradingly** | ~92% | 34 | All truncations fixed, rebranded, perf optimized, deployed | Push rebrand+perf commits, Render rename |
| **CastFreely** | ~75-80% | 423 | All 9 waves, deployed | LLC formation, SAG-AFTRA legal, Stripe |

**CLI TRUNCATION CRISIS: RESOLVED** (April 4 late). All 22 truncated files across 3 apps have been restored from git history. All apps compile/parse clean. No broken builds remain.

**Combined test count:** 2,310+ tests across Plainly Digital products
**Note:** MAPPER (245 tests) now tracked under Advisedly Compliance LLC.

---

## CROSS-CUTTING BLOCKERS

| Blocker | Affects | Action |
|---------|---------|--------|
| **No attorney review** | ALL | Consumer apps: Termly ($10/mo/site). CastFreely: entertainment attorney ($2K-5K) |
| **No insurance** | Vytally, CastFreely | E&O + GL + Cyber quotes (Hiscox, Hartford, CoverWallet) |
| **Apple/Google dev accounts** | Plainly, Vytally, 42ly, Accomplishly | $99 Apple + $25 Google, covers all apps |
| **Trademark filings** | Vytally, 42ly, Accomplishly, CastFreely | ~$350/class each |
| **CastFreely LLC not formed** | CastFreely | $300 TN filing + EIN + bank |
| **42ly DBA not registered** | 42ly | File DBA under Plainly Digital LLC |
| **RevenueCat not set up** | ALL consumer apps | One account, wire into all 4 apps |

---

## PRIORITY ACTIONS (April 4, 2026 — Updated Late Night)

**Truncation Crisis: RESOLVED.** All 22 files across 3 apps restored. All builds working.

### Immediate (Push from local terminal)

**Plainly — Push + Rebuild:**
1. `cd C:\Users\jbroc\Plainly && git push origin main` (triggers Render rebuild)
2. Run migrations on Neon: 002_add_transactions.sql through 006_fix_user_usage.sql
3. Configure Render env vars (PLAID_CLIENT_ID, PLAID_SECRET, GOOGLE_CLIENT_ID, INTERNAL_API_KEY)
4. End-to-end smoke test

**Tradingly — Push rebrand + perf:**
1. `cd C:\Users\jbroc\DayTradeScreener && git pull && git push origin master` (rebrand + perf optimization commits)
2. Rename Vercel project "frontend" → "tradingly", connect tradingly.app domain
3. Rename Render service → "tradingly-api", update ALLOWED_ORIGINS

**Accomplishly — Push truncation fix:**
1. `cd C:\Users\jbroc\Accomplishly && git pull && git push origin main` (space-detail.tsx + spaces.tsx fix)

### This Week
1. **Apple Developer ($99/yr) + Google Play ($25)** — unblocks App Store for ALL 4 apps
2. Get insurance quotes (E&O + GL + Cyber)

### Next 2 Weeks
1. RevenueCat setup (one account, wire into all apps: Free/$2.99/$6.99 + boost packs)
2. File Vytally + 42ly + Accomplishly trademarks ($350/class each)
3. CastFreely LLC formation ($300) + EIN
4. 42ly DBA registration under Plainly Digital

### Ongoing
- Vytally Phase 0 blockers (SQLite→Supabase, RLS, age gate, insurance)
- All apps: Sage 3-Layer deployed, pricing standardized, cost guards active, NIST AI RMF in place
- Plainly: Plaid production access (apply 1-2 weeks before public launch)
- Legal docs needed for 42ly, Accomplishly, Tradingly, CastFreely

**CLI MITIGATION STRATEGY:** For any file over ~80 lines, use Cowork (Edit tool) instead of CLI. CLI's truncation risk scales with file size. Use CLI only for builds, tests, git operations, and small file edits.

---

## KEY REFERENCE DOCS (by repo)

These are the canonical reference docs across all repos. Everything else has been consolidated into this tracker.

### Plainly Repo (jbrock1981/Plainly)
| Doc | Location | Purpose |
|-----|----------|---------|
| Sage Brand Personality | `docs/SAGE-BRAND-PERSONALITY.md` | Layer 1 personality spec (shared across all apps) |
| Portfolio Cost Analysis | `docs/PORTFOLIO-COST-ANALYSIS.md` | AI API cost projections across all apps |
| NIST AI Governance | `docs/NIST-AI-GOVERNANCE.md` | NIST AI RMF compliance documentation |
| AI Coach Spec | `docs/ai-coach-spec.md` | Sage coach role definition for Plainly |
| API Cost Model | `docs/api-cost-model.md` | Per-endpoint cost estimates |
| Anthropic API Compliance | `docs/anthropic-api-compliance.md` | API usage compliance notes |
| Competitive Intelligence | `COMPETITIVE_INTELLIGENCE_REPORT.md` | AI coach apps comparison (Cleo, etc.) |
| Competitive Content Analysis | `docs/competitive-content-analysis.md` | Educational content comparison (Khan, Acorns) |
| Budget/Neobank Analysis | `docs/competitive-intelligence-report.md` | YNAB, Credit Karma, Cash App comparison |
| Vytally Competitive Analysis | `HEALTH_WELLNESS_COMPETITIVE_ANALYSIS.md` | 25 health/wellness apps analyzed |
| Finlit App Plan | `docs/finlit-app-plan.md` | Original Plainly product strategy |
| Gen Z Market Research | `docs/gen-z-market-research-2025.md` | Target demographic research |
| Lesson/Module Structure | `docs/lesson-module-structure.md` | Content architecture (18 modules, 121 lessons) |
| Onboarding Wireframes | `docs/onboarding-wireframes.md` | UX wireframes |
| LLC Structure | `docs/llc-business-structure.md` | Entity structure documentation |
| Agent Conventions | `AGENT_CONVENTIONS.md` | Code style and lesson content rules |
| Income Projections | `docs/income_projections.docx` | Revenue projections |
| Launch Guide | `docs/phased_launch_guide.docx` | Phased launch plan |
| Startup Costs | `docs/startup_cost_estimate.docx` | Cost estimates |

### Tradingly Repo (jbrock1981/Tradingly)
| Doc | Location | Purpose |
|-----|----------|---------|
| Road to 100 | `ROAD_TO_100.md` | Master product roadmap (23 endpoints, 27 components, 7 priority categories) |
| Competitive Research | `COMPETITIVE_RESEARCH.md` | 8+ competitor comparison (TradingView, Finviz, Trade Ideas, etc.) |
| Advanced Features Research | `ADVANCED_FEATURES_RESEARCH.md` | GEX, dark pools, AI/ML, sentiment — API costs and feasibility |
| Final Features Research | `FINAL_FEATURES_RESEARCH.md` | Paper trading, trade journal, position calc implementation |
| Final Edge Research | `FINAL_EDGE_RESEARCH.md` | Premium features for free positioning strategy |
| Phase 9 Build Plan | `CLI_PHASE9_AND_AI.md` | Active build plan (Sage AI, cost guards, Stripe, legal) |

### Claude- Repo (jbrock1981/Claude-)
| Doc | Location | Purpose |
|-----|----------|---------|
| Legal Docs | `legal/` | Canonical Plainly Digital LLC legal templates (Operating Agreement v1-v3, IP Assignment, NDA, ToS, Privacy Policies) |

**Note:** `Claude-/docs/` contains copies of Plainly docs — the Plainly repo versions are canonical.

### Downloads
| Doc | Location | Purpose |
|-----|----------|---------|
| CastFreely Platform Plan | `CASTFREELY_PLATFORM_PLAN.md` | 18-section platform spec — should move to CastFreely repo |

---

*Updated April 4, 2026 (late night) — ALL truncation damage resolved across all 6 products. Accomplishly: 2 files restored (b648bf9), 0 TS errors. Vytally: 7 files restored (f06c5aa), 290 tests passing, user tested all 5 tabs. Tradingly: 9 Python files restored (91a17c5), rebrand complete (a781241), performance optimization with React.memo + custom hooks (681834e). Plainly truncations fixed earlier (bd6472f). Combined: 6 products, 2,310+ tests. All apps compile/parse clean. No broken builds remain. Testing mode active on all apps (pro_plus for all users). Next steps: push commits from local terminals, Render/Vercel rebuilds, then business blockers (Apple Dev, RevenueCat, insurance, legal).*
