# Glyphe (AI life advisor) — App review
**Date:** 2026-05-18
**Reviewer:** general-purpose agent (autonomous)
**Repo:** /home/jbroc/repos/42ly

## Verdict & 12-month MRR projection
Blocked-on-distribution: the code is the most polished in the portfolio, but the wedge against ChatGPT/Pi/Rosebud is thin and the category is now a regulatory minefield for anything touching minors.

| Scenario | MRR | Key assumptions |
|---|---|---|
| Conservative | $0–$120 | Beta only, no app-store launch in 12 months; RevenueCat never wired; <50 paid converts at $2.99. |
| Realistic    | $400–$900 | Soft launch Q3 2026, 5–8k installs from organic + $500/mo paid, 2.5–3.5% conversion at blended $4 ARPU, churn ~12%/mo. |
| Upside       | $2.5–4k | Gen-Z TikTok hit on the "personality calibration" angle, 30k installs, 4% paid conversion, 14-day trial actually wired, age-gated to 18+. Still <$50k ARR — not VC-grade. |

## 1. What it actually is (verified from code/repo)
- **Stack:** Expo 55 + Express TS + Supabase + Claude. Deployed on Cloud Run + Firebase Hosting (`CLAUDE.md:30`). 718 tests across 61 files.
- **Surface:** 5-tab app (Chat, Dashboard, Goals, Journal, Profile) plus a 6-domain "42 Map" radar, Decision Engine, Action Quests, persistent memory.
- **The "unique" 12-question quiz** (`lib/personality-questions.ts:10-23`) doesn't ask the user about themselves — it asks the user to *give advice* on 12 scenarios ("How would you respond if your kid said they wanted to drop out of college?"). System prompt (`server/system-prompt.ts:1-30`) is hardcoded to Jonathan Brock's persona; quiz answers feed a Layer-3 personalization string but the loop back to advisor behavior is opaque.
- **Paywall is a stub.** `app/upgrade.tsx:92-98` fires `Alert.alert('Coming Soon')` on the CTA. No RevenueCat. The "7-Day Free Trial" button does nothing.
- **Tier gating is broken.** `lib/tier.ts:21-76` gives Free, Pro, and Pro+ identical feature lists. The upgrade screen shows a 15-row comparison table where every cell is a checkmark — the opposite of a paywall.

## 2. Functionality critique
**Grade:** B-
- **What works:** (1) Streaming Claude chat with the portfolio's most-hardened crisis detection (`server/crisis-detection.ts`, 55+ patterns, unicode/homoglyph/l33tspeak tests). (2) Hybrid Supabase + AsyncStorage CRUD with real offline fallback. (3) 6-domain radar dashboard with weekly trend arrows.
- **What's broken:** (a) RevenueCat not wired (`app/upgrade.tsx:92-106`). (b) Tiers are cosmetic — `lib/tier.ts:21-76` gates nothing. (c) Parental controls PARTIAL per `CLAUDE.md:187`: `isMinor` collected, no consent flow — a launch-blocker post-SB 243. (d) No Privacy Policy or ToS in repo.
- **Where a real user gets stuck:** Tap "Start 7-Day Free Trial" → `Coming Soon` alert. That's the entire revenue funnel.
- **Competitive moat — the 12-q quiz:** No. ChatGPT GPT-5.5 now ships personality presets (Default/Friendly/Efficient/Professional/Candid/Quirky) on every tier plus memory sources across all consumer plans. A 12-question one-shot calibration is *less* personalized than what ChatGPT does passively. Worse, the questions ask the user to be the advisor — clever idea, but it risks making the advisor sound like a mirror of the user's stated values, which collapses the "tough love dad" pitch.
- **Test coverage:** 718 tests is impressive for a solo build but skews to safety/guardrails and storage. No E2E auth test (own admission), no integration test against a live Claude call, and no test confirming the quiz answers actually change advisor behavior. Passing tests do not equal a shipped product.

## 3. Sellability critique
**Grade:** D+
**Target user:** Gen-Z (16–27) per `server/system-prompt.ts:27`. Post-SB-243 reality: 18–24, anxious, has tried ChatGPT and BetterHelp, lives on TikTok, willing to pay <$10/mo for "an AI that gets me."
**Alternative today:** ChatGPT free with GPT-5.5 + Personality Presets + memory sources ($0). Pi by Inflection ($0, no limits). Rosebud ($6M Bessemer-backed) for journaling. Replika ($19.99/mo or $70/yr, category retention leader). Headspace Ebb ($69.99/yr bundled). Athena AI Life Advisor already on both stores.

ChatGPT free is the elephant. A Gen-Z user can already set a "Candid" preset, have ChatGPT remember "I want tough-love-dad energy," carry that across conversations indefinitely, $0, on a UI they're already in 5x/day. Glyphe's only credible differentiation is the 6-domain radar and quest auto-generation — visualizations, not AI capabilities.
**Reason they'd switch:** None compelling at $2.99/mo today. Possible if the radar/quest visualization surfaces patterns ChatGPT can't ("your Relationships domain dropped 30% in 4 weeks").
- **Pricing fit:** $2.99 is roughly right for the value but the anchor is wrong — Pi free + ChatGPT free mean any non-zero price needs a sharp wedge. $2.99 is too low to fund paid acquisition and too high to beat free.
- **Value prop (writing it because repo lacks one):** *"A private AI life coach that maps the 6 areas of your life and tells you the one thing to fix this week — no scrolling, no homework, no therapist bills."*
- **First 100:** Jonathan's network + invite-only beta. Realistic.
- **First 1000:** Brutal. Either TikTok organic on the "AI dad" angle, a $500–1000 paid test at $2–4 CPI, or one Reddit hit. Without a viral wedge, stalls at <500.
- **Viral mechanics:** None. No shareable quiz result card, no referral. The quiz output is the most natural viral artifact and it isn't shareable.

## 4. Top 3 monetization opportunities (URL + date required)
1. **One-time "Life Map" IAP at $9.99–14.99 (Patet Certified pattern).** Subscriptions die at week 3 — 66% 30-day drop-off across AI companions (digitalhumancorp.com/en/research/best-ai-companion-app-2026, 2026); one-shot IAPs survive churn. **MRR (amortized):** $200–600. **Effort:** 4 days.
2. **Annual plan + real 7-day trial wired to RevenueCat.** Replika's $70/yr annual is the conversion vehicle vs. monthly (aicompanionguides.com/blog/replika-review/, 2026). Glyphe already prices $24.99/$57.99 yr — the button just doesn't work. **MRR:** $300–800. **Effort:** 5 days.
3. **B2B school/youth-org licensing pivot.** Headspace licenses Ebb to 2,000+ employers under a stratified-care model (organizations.headspace.com/blog/transforming-workforce-mental-health-with-our-new-ai-powered-stratified-care-model, 2026). One $200/mo school beats 67 individual $2.99 subs and sidesteps the SB-243 minor-targeting trap. **MRR:** $400–2000. **Effort:** 10–15 dev days + sales cycle.

## 5. Top 3 functionality fixes (highest leverage)
1. **Fix `lib/tier.ts` so Free/Daily/Deep actually differ.** Today every cell of the comparison table is a checkmark — fatal for conversion. Effort: 1 day.
2. **Wire RevenueCat + kill the `Coming Soon` alert in `app/upgrade.tsx`.** No revenue ships without this. Effort: 3–5 days (SDK, products, sandbox, restore, server-side receipt validation against `cost-guard.ts`).
3. **Make the 12-question quiz produce a shareable "Your Life Advisor" result card.** Today the calibration is invisible to the user. A shareable PNG is the only plausible viral loop on a no-gamification app. Effort: 4 days.

## 6. Competitive landscape (2026)
| Name | Pricing | Funded? | Recent 2026 move | What they do better | What they miss |
|---|---|---|---|---|---|
| ChatGPT (OpenAI) | Free / $20 Plus | $122B raise at $852B post-money (Sep 2025) | GPT-5.5 + Personality Presets + Memory Sources on all tiers (2026) | Scale, brand, distribution, model quality, free memory | Domain-specific structure, life-mapping, opinionated persona |
| Character.AI | Free / $9.99 c.ai+ | Settled teen-suicide suits Jan 2026; banned under-18s in response | Under-18 ban after lawsuits (NBC News, 2026) | Massive character library, voice | Adult-only post-ban; no life-advisor positioning |
| Replika | Free / $19.99/mo / $299 lifetime | FTC complaint Jan 2025; €5M GDPR fine May 2025 | 8+ month emotional memory leadership (aicompanionguides, 2026) | Memory retention, relationship-bond UX | Reputation toxicity, regulatory overhang |
| Pi (Inflection) | Free, no limits | Acquired by Microsoft 2024 | "No-advice-unless-asked" consumer life-stress positioning (Lindy review, 2026) | Free, no friction, zero churn pressure | Monetization unclear — competing with $0 is brutal |
| Rosebud | ~$8–10/mo | $6M from Bessemer | Therapist-designed workbooks + memory + intention setting (2026 Rosebud reviews) | Journaling-first, conversational, retention design | No domain dashboards, no advisor persona |
| Headspace Ebb | $69.99/yr bundled | Headspace mature, public-adjacent | Voice mode rollout Dec 2025; 2,000+ employer distribution (BusinessWire) | Distribution, clinical credibility | Bundled — not standalone, not Gen-Z native |

## 7. Honest "DO NOT do" list
1. **Do not target under-18 users.** CA SB 243 (eff. 2026-01-01): $1,000+/violation + private right of action. NY AI companion law: $15,000/day. GUARD Act in Congress. Character.AI banned minors after settled teen-suicide suits. The 16–27 target in the system prompt + the `isMinor` collection-without-enforcement gap are legal landmines. Re-target 18–24 and gate hard.
2. **Do not add voice mode just because Ebb and Character.AI did.** Table-stakes, not differentiation, and it doubles per-session inference cost. Ship after IAP.
3. **Do not add an avatar / virtual companion UI.** That category is now defined by lawsuits. "Tough love dad" is defensible positioning — keep it boring on purpose.
4. **Do not chase TikTok quiz-virality without a shareable artifact first.** Personality quizzes are the highest-converting marketing format, but only if the result shares. Don't burn ad budget against a quiz whose output never leaves the app.
5. **Do not raise a seed for this.** Series A in AI now requires a defensible moat (Gizmo $22M, May 2026), and Glyphe is feature-equivalent to ChatGPT free + a radar chart. Bootstrap; let Patet/Winlet/Vinla carry the portfolio.

## 8. Sources
- WeavAI, Replika AI Review 2026, 2026-04-16 — https://weavai.app/blog/en/2026/04/16/replika-ai-review-2026-features-pricing-analysis/
- AICompanionGuides, Replika Review ($70/yr), 2026 — https://aicompanionguides.com/blog/replika-review/
- StartupHub, Character AI Review 2026 — https://www.startuphub.ai/ai-news/reviews/2026/character-ai-review-2026
- DigitalHumanCorp, Best AI Companion Apps 2026 (66% drop-off) — https://digitalhumancorp.com/en/research/best-ai-companion-app-2026
- a16z, Top 100 Gen AI Consumer Apps March 2026 — https://a16z.com/100-gen-ai-apps-6/
- Lindy, ChatGPT Alternatives 2026 (Pi free positioning) — https://www.lindy.ai/blog/chatgpt-alternative
- Headspace, Ebb ($69.99/yr) — https://www.headspace.com/headspace-subscription/ebb
- BusinessWire, Ebb voice mode, 2025-12-08 — https://www.businesswire.com/news/home/20251208896917/en/Headspace-Rolls-out-Voice-Feature-for-Empathetic-AI-Companion-Ebb
- Headspace, Stratified Mental Health Model (2,000+ employers) — https://organizations.headspace.com/blog/transforming-workforce-mental-health-with-our-new-ai-powered-stratified-care-model
- Rosebud (Bessemer $6M) — https://www.rosebud.app/
- NPR, Pennsylvania v. Character.AI, 2026-05-05 — https://www.npr.org/2026/05/05/nx-s1-5812861/characterai-chatbot-medical-advice-pennsylvania-lawsuit
- NBC News, Character.AI bans minors — https://www.nbcnews.com/tech/tech-news/characterai-bans-minors-response-megan-garcia-parent-suing-company-rcna240985
- Fortune, Google/Character.AI settle teen-suicide suits, 2026-01-08 — https://fortune.com/2026/01/08/google-character-ai-settle-lawsuits-teenage-child-suicides-chatbots/
- California Lawyers Assn., AI companion regulation 2026 (SB 243, GUARD Act, NY law) — https://calawyers.org/privacy-law/regulatory-focus-on-ai-companion-character-chatbots/
- Suprmind, ChatGPT 2026 Features (memory, presets) — https://suprmind.ai/hub/chatgpt/features/
- Beginners in AI, ChatGPT 2026 (GPT-5.5, Memory Sources) — https://beginnersinai.org/whats-new-chatgpt-2026/
- Angel Investors Network, Gizmo $22M Series A, May 2026 — https://angelinvestorsnetwork.com/startups/series-a-ai-native-ed-tech-startup-funding-2026
- Athena AI Life Advisor (App Store) — https://apps.apple.com/us/app/athena-ai-life-advisor/id1668456320
- TechCrunch, Google Health Coach $9.99/mo, 2026-05-07 — https://techcrunch.com/2026/05/07/googles-9-99-per-month-ai-health-coach-launches-may-19/
