# Patet — App review
**Date:** 2026-05-18
**Reviewer:** general-purpose agent (autonomous)
**Repo:** /home/jbroc/repos/Plainly

## Verdict & 12-month MRR projection

Ship to TestFlight this week, but recognize that OpenAI launched ChatGPT + Plaid bank-aware finance on 2026-05-17 (same day Patet's Plaid prod creds landed). "AI that reads your bank" is a commodity by Q3. Patet's defensible angle is curriculum + Plaid + persona + Certified credential, especially in Spanish. Blocked-on-launch: RevenueCat config, store records, leftover Dev tier toggle on `app/app/upgrade.tsx:277`.

| Scenario | MRR | Key assumptions |
|---|---|---|
| Conservative | $180 | 5K installs organic-only; 1.5% paid; blended ARPU $2.40 |
| Realistic | $850 | 18K installs/12mo (LATAM Spanish lift); 2.0% paid; 70% Connected / 30% Coached; +$40/mo affiliate; ~5 Certified IAPs/mo at $19 |
| Upside | $2,400 | One viral TikTok moment; 60K installs; 2.5% paid; LATAM day-90; Patet Certified™ wins one CU/college pilot |

Realistic is the planning number. Fintech CPI is $10–$35 per Adaction 2026, so $50/app means 100% organic + referral.

## 1. What it actually is (verified from code/repo)
- 18 modules / 121 lessons EN+ES, 5 calculators, AI coach with 4 unlock-gated personas — confirmed via `app/constants/modules.ts`, `server/src/lib/unlocks.ts`, `app/app/upgrade.tsx`.
- The three must-haves are shipped, not just planned: `server/src/services/moneyWrapped.ts` (Sunday cron + Haiku/Sonnet recap), `paydayCoach.ts` (Plaid paycheck classification + auto-coach), `subscriptionDetector.ts` + `subscriptionActions.ts` (cancellation script).
- Patet Certified™ is real: 50-question assessment, `paid_at IS NULL` pending state, RC product `patet_certified_credential` at $19, LinkedIn add helper. Nothing comparable at Cleo / Rocket / Monarch.
- Pricing rename live in user copy; tier codes unchanged in DB/RC.
- 1,043 tests / 68 suites for a solo-dev pre-beta is high.

## 2. Functionality critique
**Grade:** B

- **What works (top 3):** (1) Coach + persona overlay + crisis detection + guardrails — `moneyWrapped.ts` re-uses `buildSystemPrompt` so the persona ladder rides into the recap. (2) Plaid path: MFA-gated link token, AES-256-GCM token encryption, ES256-JWT webhook verification, paycheck-confirmation step. (3) Tier gating is real — `requireTier.ts` enforces server-side, not just UI hides.
- **What's broken / unfinished:**
  - `app/app/upgrade.tsx:277-279` "Dev: cycle tier" button visible to every user. Remove before App Review.
  - `render.yaml` Blueprint never imported (CLAUDE.md Pre-Beta Blockers). Onboarding-email cron does not fire in prod. Money Wrapped Sunday cron has the same dependency — silent no-ops.
  - PII Phase B blocked on backfill that hasn't run.
  - `REVENUECAT_WEBHOOK_AUTH` + `GOOGLE_CLIENT_ID` still empty on Render. Without webhook auth, subscription state is forgeable.
  - Spanish lesson bodies machine-translated, no native LATAM reviewer pass. Don't market LATAM until that closes.
- **Where users get stuck:** MFA setup is enforced BEFORE Plaid Link (mig 023). Will cost 15–25% of activation. Most consumer apps do MFA opt-in post-link.
- **Performance:** Render free tier cold-starts at 30s — Sunday Money Wrapped push into cold API is a first-impression killer. Add keep-alive or migrate to Cloud Run.
- **Tests:** 1,043 reads great but is mostly unit/contract. No Detox / Playwright e2e. Add a synthetic that hits the cron endpoint weekly and pages on zero deliveries — silent silence is the failure mode unit tests miss.

## 3. Sellability critique
**Grade:** C+

**Target user:** 22–27-year-old first-or-second-job W-2 making $45K–$75K, 1–3 cancelable subscriptions, one revolving credit card balance, bilingual or US Hispanic. Tried Cleo (too meme) or Rocket (too narrow), uses both.

**Alternative today:** Rocket Money Premium at $7/mo sliding for cancellation; free Cleo for the chat.

**Reason they'd switch:** Patet bundles curriculum + Plaid-aware coach + subscription cancellation at $2.99 — a third of Rocket's floor, a fifth of YNAB/Monarch's $14.99. Surface "Rocket charges $7. We charge $2.99." on the upgrade screen or you're leaving the wedge on the floor.

- **Pricing fit:** Connected $2.99 sharp. Coached $6.99 is tougher — Sonnet-50/mo is an internal cost cap, not a user-legible benefit. Reframe Coached as "weekly Money Wrapped + payday auto-coach + premium model."
- **Value prop:** Existing promo "An AI coach that actually knows what you're spending on" is good. Test "Patet: Money Coach + Bank" as App Store name — "AI Money Coach" is saturated as of 2026-05-17 ChatGPT launch.
- **First 100:** Friends/family TestFlight (5–10), college refs, one r/personalfinance + r/povertyfinance post, one Money Roast TikTok with 3 UI cuts.
- **First 1000:** LATAM Spanish listing day-90 is highest-EV — Cleo and Rocket are English-strong; native Spanish parity is unbeatable on a $50 budget. Patet Certified™ + one CU/college pilot is #2.
- **Viral:** Money Roast share + 50-call referral are weak primitives. Add subscription-cancellation share ("Saved $X/yr"), Money Wrapped share, Patet Certified™ LinkedIn add.

## 4. Top 3 monetization opportunities

1. **Reframe Connected as Rocket Money undercut.** Rocket Premium runs $7–$14/mo headlining cancellation [https://help.rocketmoney.com/en/articles/2217739 — 2026-05-18]. Patet Connected $2.99 includes that + curriculum + Plaid coach. Add a "Rocket $7 / Patet $2.99" compare row above the tier cards. **MRR:** +$200/mo by month 6. **Effort:** 2 days.

2. **Patet Certified™ → CU / community-college license.** Zogo's model is co-branded license fees to credit unions [https://nextcity.org/urbanist-news/financial-literacy-app-helps-credit-unions-connect-with-gen-z — 2026-05-18]. Patet has the 50-q assessment + LinkedIn credential Zogo doesn't. One $2.4K/mo license = +$2.4K MRR. **MRR:** +$1.2K–$2.4K from 1 pilot in months 6–9. **Effort:** ~15 days (sales, not code).

3. **Spanish-localized App Store listing post-reviewer-pass.** Cleo hit 8M users and $500M valuation on English-only Gen Z [https://www.fintechfutures.com/fintech-innovation/gen-z-financial-assistant-app-cleo-raises-80m-at-500m-valuation — 2026-05-18]. LATAM-Spanish in finance is near-empty; Patet has 121 lessons translated. **MRR:** +$300/mo by month 12 if reviewer pass ($2K–$5K cash) bumps ES installs 4–6×. **Effort:** ~3 dev days + $2K–$5K cash.

## 5. Top 3 functionality fixes (highest leverage)

1. **Gate the Dev tier toggle.** Remove or `__DEV__`-gate `app/app/upgrade.tsx:277-279`. Misleads users and risks App Review rejection. **Effort:** 30 min.

2. **Wire Money Wrapped + email crons via Render Blueprint or in-process scheduler.** Blueprint has never been imported per CLAUDE.md. The whole retention thesis depends on Sunday push firing — today it doesn't. **Effort:** 1 day ops, 0 code.

3. **Defer MFA until after first Plaid Link succeeds.** Mig 023 forces TOTP before bank link. For a no-money-movement app, that's theater at the highest-friction step. Link first, then prompt MFA on next session, step-up only on sensitive writes. **Effort:** 3 days.

## 6. Competitive landscape (2026)

| Name | Pricing | Funded? | Recent 2026 move | What they do better | What they miss |
|---|---|---|---|---|---|
| Rocket Money | Free / $7–$14/mo sliding | Acquired by Rocket Companies 2021 | Subscription concierge cancellations [https://www.rocketmoney.com/feature/manage-subscriptions] | Actual human concierge for cancellations | No curriculum, no AI coach, no Spanish parity |
| YNAB | $14.99/mo, $99/yr | Bootstrapped | Free for college students with .edu [https://thecollegeinvestor.com/32672/best-budgeting-apps/ — 2026-05-18] | Zero-based budgeting philosophy + dogmatic community | No Plaid-aware AI, no Spanish, 5× Patet's price |
| Monarch Money | $99/yr base, $199/yr Plus | Series A | Launched Monarch Plus tier 2026-04-21 [https://thinksaveretire.com/monarch-money-review/ — 2026-05-18] | Household + couples mode | Couples-first means solo Gen Z user is second-class |
| Copilot | $13/mo, $95/yr | $10.5M Series A Mar 2024 (no 2026 round) [https://copilot.money/series-a] | iOS-only premium-design lock-in | Apple-aesthetic UX, fastest iPhone categorization | Android-null, no Spanish, no curriculum |
| Cleo | Free / $14.99/mo | $175M total, $500M valuation [https://www.fintechfutures.com/fintech-innovation/gen-z-financial-assistant-app-cleo-raises-80m-at-500m-valuation] | 8M users 2026, 74M+ conversations in 2024 | Brand voice / meme energy / Roast | No curriculum, no Plaid-driven lesson rec, lender/cash-advance product confusion |
| ChatGPT (Plaid bank) | $20/mo ChatGPT Plus | OpenAI | Bank-linked finance launched 2026-05-17 [https://winbuzzer.com/2026/05/17/openai-launches-chatgpt-for-personal-finance-will-xcxwbn/] | Brand, distribution, model quality | No curriculum, no shareable credential, no persona laddering, no domain guardrails |

## 7. Honest "DO NOT do" list

1. **Don't chase OpenAI on model quality.** ChatGPT+Plaid launched 2026-05-17 and will beat Sonnet 4.6 in raw capability inside 90 days. Patet's moat is curriculum + persona + credential + Spanish + sub-$3 floor.
2. **Don't build social/community for v1.** Solo dev + $50/app can't moderate a feed. `MUST-HAVE-PLAN.md` correctly puts social moats at Phase 5.
3. **Don't spend on paid installs.** Fintech CPI $10–$35 [https://www.adaction.com/blog/mobile-app-user-acquisition-cost — 2026-05-18]; $50 = 1–5 installs, ~0 paid users. 100% organic + referral.
4. **Don't wire XP/badges/leaderboard UI.** CLAUDE.md Rule 6. Gen Z tester feedback already in.
5. **Don't ship Money Movement / Plaid Transfer / cash advance.** Cleo's biggest 2026 risk is lender-confusion. "We can't move your money" is a clean Patet differentiator.

## 8. Sources

- https://intelmarketresearch.com/financial-literacy-gamification-app-for-gen-z-market-44708 — 2026-05-18
- https://www.whistl.app/blog-best-finance-apps-gen-z-2026.html — 2026-05-18
- https://www.bestmoney.com/financial-advisor/learn-more/best-ai-budgeting-apps — 2026-05-18
- https://thecollegeinvestor.com/32672/best-budgeting-apps/ — 2026-05-18
- https://www.thepennyhoarder.com/budgeting/budgeting-copilot-money-review/ — 2026-05-18
- https://www.thepennyhoarder.com/budgeting/rocket-money-review/ — 2026-05-18
- https://www.rocketmoney.com/feature/manage-subscriptions — 2026-05-18
- https://help.rocketmoney.com/en/articles/2217739-how-much-does-rocket-money-cost — 2026-05-18
- https://winbuzzer.com/2026/05/17/openai-launches-chatgpt-for-personal-finance-will-xcxwbn/ — 2026-05-17
- https://www.pymnts.com/artificial-intelligence-2/2026/perplexity-uses-plaid-to-personalize-money-insights/ — 2026-05-18
- https://plaid.com/blog/chatgpt-personal-finance-plaid/ — 2026-05-18
- https://www.businessofapps.com/data/finance-app-benchmarks/ — 2026-05-18
- https://unstar.app/blog/app-retention-benchmarks-2026 — 2026-05-18
- https://www.fintechfutures.com/fintech-innovation/gen-z-financial-assistant-app-cleo-raises-80m-at-500m-valuation — 2026-05-18
- https://thinksaveretire.com/monarch-money-review/ — 2026-05-18
- https://copilot.money/series-a — 2026-05-18
- https://nextcity.org/urbanist-news/financial-literacy-app-helps-credit-unions-connect-with-gen-z — 2026-05-18
- https://www.adaction.com/blog/mobile-app-user-acquisition-cost — 2026-05-18
- https://prospeo.io/s/fintech-customer-acquisition-cost — 2026-05-18
