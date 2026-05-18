# Vinla — App review
**Date:** 2026-05-18
**Reviewer:** general-purpose agent (autonomous)
**Repo:** /home/jbroc/repos/Vytally

## Verdict & 12-month MRR projection
Blocked-on-IAP-and-distribution: tech is better than the brief implies (server-side cost guard exists, Postgres migrated 2026-04-20), but with Cal AI now owned by MyFitnessPal at ~$50M ARR, a solo-dev food-vision app with $50/mo ad budget has no path to meaningful MRR without a sharper wedge.

| Scenario | MRR | Key assumptions |
|---|---|---|
| Conservative | $0–$120 | Family beta only, never ships, BETA_PRO_ACCESS stays on |
| Realistic    | $150–$450 | Ships Q3 2026 w/ RevenueCat IAP; 200–800 installs; 2.5% D35 paid conv |
| Upside       | $1,200–$2,500 | Repositions on experiments framework; 3K installs via one influencer; 6% paid conv |

Realistic case doesn't cover Anthropic + Vercel + EAS costs at Peak Sonnet usage. Only works if 80%+ stay on Haiku.

## 1. What it actually is (verified from code/repo)
- React Native + Expo SDK 53, 22 screens, Zustand persistence. Health data in on-device SQLite via Drizzle (`src/db/`); only `users`, `password_reset_tokens`, `user_usage` server-side in Neon (`api/_lib/schema.sql`).
- Auth is **custom JWT against Neon**, NOT Supabase — brief is stale. `package.json` has `@neondatabase/serverless` + `bcryptjs` + `jsonwebtoken`, no `@supabase/*`. `api/_lib/auth.ts` verifies bearer JWT only.
- AI: Haiku 4.5 default; Sonnet 4.6 for Pro+ chat with 50/mo cap via atomic filtered UPDATE (`cost-guard.ts:353-375`). Food vision (`api/food-vision.ts`) is Haiku-only with hard clamps (5000 kcal / 500g per macro) and forces `confidence: 'low'` on clamp.
- Tier enforcement is **server-side and atomic** via `costGuard()` (reset-then-filtered-UPDATE, `cost-guard.ts:183-342`). Brief's "client-side tier CRITICAL" claim is wrong for AI cost. Real exposure: **subscription state** — `PaywallScreen.tsx:65-73` calls `upgradeToPro()` on tap with no receipt; `BETA_PRO_ACCESS=true` server-side (`cost-guard.ts:72`) grants every user Pro+.
- 373 test/it assertions across 19 Jest files (brief's "364 tests" out of date). Cover cost-guard races, crisis detection, server-side system-prompt assembly, vision clamping.

## 2. Functionality critique
**Grade:** B-

- **Works end-to-end:** (1) race-safe atomic cost guard with Sonnet-cap enforcement — production-grade; (2) food vision with sanity clamps + confidence downgrade; (3) 2-layer crisis detection + mid-stream output guardrail redaction + upstream abort on client-close (`api/chat.ts:139-200`).
- **Broken/unfinished:**
  - **No real IAP.** `PaywallScreen.tsx:65-73` `handleRestore` just calls `upgradeToProPlus()` locally. No StoreKit, no RevenueCat. This is THE blocker.
  - **`BETA_PRO_ACCESS=true` in both layers** (`subscriptionStore.ts:78`, `cost-guard.ts:72`). Every install gets Pro+ Sonnet free; at $3/$15 Mtok Sonnet pricing, ~$0.50/user/mo bleed.
  - **SQLite only for health data.** New device = empty app. No cohort/retention server-side.
  - **App Store credentials empty** in `eas.json` (appleId, ascAppId, appleTeamId blank).
- **UX dead-ends:** New device loses 100% of log history. Restore Purchase toggles tier on tap with no validation — fails App Review.
- **Security (blast-radius ranked):**
  1. No IAP receipt verification — paywall decorative. Blast radius = 100% of revenue.
  2. JWT secret has no kid-based rotation. Compromise = forced re-login, livable.
  3. No RLS on Neon — irrelevant; per-user health data is on-device. Neon tables touched only via parameterized server SQL. Brief's "RLS CRITICAL" is a Supabase-era artifact.
  4. Age gate missing — hard App Store blocker under 2026 Utah/Texas/Louisiana laws + Apple Family Sharing flow ([loeb.com 2025-12](https://www.loeb.com/en/insights/publications/2025/12/app-store-age-verification-laws-trigger-new-federal-and-state-childrens-privacy-requirements)).
- **Tests:** 373 assertions / 19 suites is solid, but they cover libraries more than user flows. No e2e for "tap upgrade → IAP → server tier flip" because that flow doesn't exist.

## 3. Sellability critique
**Grade:** D+

**Target user:** Self-experimenting adults 28–45 with GI issues, perimenopause symptoms, sleep problems, or post-diagnosis chronic conditions — already tracking, want a coach connecting sleep ↔ food ↔ mood. NOT "general wellness" — MFP+Cal AI owns that.

**Their alternative:** MyFitnessPal Premium $19.99/mo or $79.99/yr (now bundled with Cal AI photo recognition post-2026-03-02 acquisition). Cronometer Gold $9.99/mo or $49.99/yr for deep-nutrient users. ([nutriscan.app 2026](https://nutriscan.app/blog/posts/cheapest-nutrition-app-2026-pricing-compared-4c18a9205d), [techcrunch 2026-03-02](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens/))

**Reason they'd switch:** Today, nothing. Vinla is undifferentiated. The ONLY credible wedge in the code is the **experiments framework** (test one variable, 7-day cycle) — not in MFP. Lead with that, not food photos.

- **Pricing fit:** $2.99/$6.99 is below MFP and Noom — not a moat, a signal of "don't know our customer." RevenueCat 2026: H&F sells 68% annual, annual renewal 25%. At $24.99/yr after Apple cut and 25% renewal: ~$6.25 LTV. CAC must be <$2 to hit 3:1. ([revenuecat 2026](https://www.revenuecat.com/state-of-subscription-apps/), [foundrycro 2026](https://foundrycro.com/blog/ltv-cac-ratio-benchmarks-2026/))
- **Value prop:** "Run a 7-day experiment on one variable; Vinla tells you what actually moved." (Currently: "unlock your full health journey" — generic.)
- **First 100:** Family + network + one r/QuantifiedSelf post. Reachable.
- **First 1000:** Not on $50/mo Meta. One N=1-adjacent influencer (Attia/Johnson sphere) at $300–$800 is the honest path.
- **Viral:** Vinla Wrapped + Health Story share card. Verify the share card looks good — free distribution.

## 4. Top 3 monetization opportunities (URL + date required for each)
1. **Reposition on the experiments framework**
   - *Data:* Specialized fitness apps reach 25% D30 retention vs. 3% for general wellness; D35 download-to-paid NA median 2.56%. Niche lifts both. ([revenuecat 2026](https://www.revenuecat.com/state-of-subscription-apps/), [businessofapps 2026](https://www.businessofapps.com/data/health-fitness-app-benchmarks/))
   - *Incremental MRR:* +$200–$400/mo at 1K installs.
   - *Effort:* 3–5 days (copy + paywall + onboarding reshuffle, no new code).

2. **Annual default + 17-day trial**
   - *Data:* Trial-to-paid 25.5% at ≤4 days vs. 42.5% at 17–32 days; H&F sells 68% annual. ([revenuecat 2026](https://www.revenuecat.com/state-of-subscription-apps/))
   - *Incremental MRR:* +30–50% on paid conv; ~$80–$150/mo lift.
   - *Effort:* 1 day (default `selectedPlan` to `pro_yearly`, extend trial to 17d).

3. **Boost packs as primary upsell**
   - *Data:* Subscription fatigue is a top-10 killer in RC 2026; Cal AI's run came from low-friction purchase intent. ([revenuecat 2026 trends](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026/))
   - *Incremental MRR:* $50–$150/mo from non-subscribers paying $1.99 for "+50 scans."
   - *Effort:* 2 days — boost packs already exist; surface on food-vision empty state.

## 5. Top 3 functionality fixes (highest leverage)
1. **RevenueCat IAP + remove BETA_PRO_ACCESS.** Pre-launch blocker. Every install is currently free Pro+; App Review rejects empty StoreKit. Effort: 5–7 days (RC SDK, both stores, server webhook → `user_usage.tier`, regression test BETA flag removal in both files).

2. **18+ age gate (not 13+).** Pre-launch blocker. 2026 state laws require <13/13–15/16–17/18+ sorting and Family Sharing parental consent for <13. Pick adult-only to dodge COPPA entirely. Effort: 2 days (DOB at signup, hard block <18, ToS). ([loeb.com 2025-12](https://www.loeb.com/en/insights/publications/2025/12/app-store-age-verification-laws-trigger-new-federal-and-state-childrens-privacy-requirements))

3. **Opt-in server-side log sync (analytics-only).** Without it, no D7/D30 retention measurement. Keep SQLite as source-of-truth; sync {date, log_type, value_summary} to Neon. Effort: 4–6 days. (Defer: full cloud↔device sync — quarter of work, not needed for v1.)

## 6. Competitive landscape (2026)
| Name | Pricing | Funded? | Recent 2026 move | What they do better | What they miss |
|---|---|---|---|---|---|
| MyFitnessPal + Cal AI | $19.99/mo, $79.99/yr | Owned by Francisco Partners; Cal AI acquired 2026-03-02 ([techcrunch.com](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens/)) | Integrated Cal AI photo recog into MFP database (20M foods, 68.5K brands) | Distribution, brand, food DB depth | Coaching, behavioral experiments, mood/sleep correlation |
| Noom | $17.40/mo ($209/yr) | Public-adjacent; Noom Med GLP-1 expansion 2026 | Optional GLP-1 access bundled | Behavioral psychology curriculum, weight-loss positioning | Photo food, true AI coach |
| Cronometer | $9.99/mo, $49.99/yr ([nutrifytracker.com 2026](https://nutrifytracker.com/blog/cronometer-vs-mfp)) | Bootstrapped, profitable | Custom nutrient targets, biometric tracking, fasting timers | Nutrient depth (USDA + custom), chronic-condition crowd | Coaching, conversational AI |
| Cal AI (pre-acq) | $9.99/mo, $39.99/yr | $50M ARR ([inc.com 2026](https://www.inc.com/ben-sherry/he-built-an-ai-app-in-high-school-made-40m-and-sold-to-myfitnesspal-now-hes-aiming-even-bigger/91307748)) | Sold to MFP 2026-03 | Photo speed, viral playbook | Now absorbed |
| PlateLens | $7.99/mo ([ai-food-tracker.com](https://ai-food-tracker.com/)) | Stealth | 94.3% food ID, ±1.2% portion | Vision accuracy leader | Coaching, sleep/mood |

Vinla loses head-to-head on food vision. Wins only on (a) price (a curse, not a moat) and (b) experiments framework — which nobody on this list has.

## 7. Honest "DO NOT do" list
1. **Don't chase Cal AI / PlateLens on food-vision accuracy.** Haiku 4.5 + clamps will lose that race. Position food photo as convenience inside the experiments framework.
2. **Don't add a community/social feed.** Accountability partners is enough. A feed needs moderation + crisis-escalation pipeline; 0 users will post at family-beta scale.
3. **Don't add GLP-1 / Ozempic content.** Noom Med has a clinical org. Mentioning GLP-1s pushes you toward FDA medical-device territory. Stay wellness-side per CLAUDE.md's own rule.
4. **Don't lower price further.** $2.99/$6.99 is already below market. Discounting trains users to expect free. Push annual instead.
5. **Don't ship web-paywall.** Mobile IAP only — web opens tax nexus, payment-processor accounts, and support load.

## 8. Sources
- [Best Calorie Tracking Apps 2026 (kcalm.app)](https://www.kcalm.app/blog/best-calorie-tracking-apps-comparison/) — accessed 2026-05-18
- [Cheapest Nutrition App 2026 — Pricing Compared (nutriscan.app)](https://nutriscan.app/blog/posts/cheapest-nutrition-app-2026-pricing-compared-4c18a9205d) — accessed 2026-05-18
- [MyFitnessPal acquires Cal AI (TechCrunch, 2026-03-02)](https://techcrunch.com/2026/03/02/myfitnesspal-has-acquired-cal-ai-the-viral-calorie-app-built-by-teens/) — accessed 2026-05-18
- [Cal AI $40M revenue, sold to MyFitnessPal (Inc.com)](https://www.inc.com/ben-sherry/he-built-an-ai-app-in-high-school-made-40m-and-sold-to-myfitnesspal-now-hes-aiming-even-bigger/91307748) — accessed 2026-05-18
- [Cronometer vs MyFitnessPal 2026 (nutrifytracker.com)](https://nutrifytracker.com/blog/cronometer-vs-mfp) — accessed 2026-05-18
- [RevenueCat State of Subscription Apps 2026](https://www.revenuecat.com/state-of-subscription-apps/) — accessed 2026-05-18
- [RevenueCat 2026 trends summary](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026/) — accessed 2026-05-18
- [Health & Fitness App Benchmarks 2026 (Business of Apps)](https://www.businessofapps.com/data/health-fitness-app-benchmarks/) — accessed 2026-05-18
- [LTV:CAC Ratio Benchmarks 2026 (Foundry CRO)](https://foundrycro.com/blog/ltv-cac-ratio-benchmarks-2026/) — accessed 2026-05-18
- [App Store Age Verification Laws 2025-12 (Loeb & Loeb LLP)](https://www.loeb.com/en/insights/publications/2025/12/app-store-age-verification-laws-trigger-new-federal-and-state-childrens-privacy-requirements) — accessed 2026-05-18
- [KOSA / App Store Accountability Act 2026 (Fortune, 2026-03-18)](https://fortune.com/2026/03/18/kosa-kids-act-app-store-accountability-act-minors-age-verification/) — accessed 2026-05-18
- [PlateLens accuracy benchmark](https://ai-food-tracker.com/) — accessed 2026-05-18
