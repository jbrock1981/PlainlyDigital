# Portfolio app review synthesis — 2026-05-18

**Source reviews:** 8 individual app reviews in this directory. Each is ~1,500 words; total ~14,500. This synthesis pulls the cross-cutting findings.

**Method:** 8 parallel general-purpose agents, each grepped its repo + ran live 2026 web searches with URL+date citations. Every market claim in this doc traces back to a specific review's §8 sources.

---

## TL;DR

- **Best single-app upside: Patet** — $850/mo realistic, $1.5-3K with B2B Certified™ pivot. Still the strongest bet.
- **4 of 8 apps need B2B pivots to clear $1K MRR.** Winlet (Slack/Teams), Glyphe (schools), Salvis (pharmacy/AL facilities), Fraus (RIAs/senior-living). Consumer-only ceilings are sub-$1K.
- **2 apps have NO working revenue path in code today.** Glyphe (`upgrade.tsx` fires `Alert.alert('Coming Soon')`) and Vinla (`PaywallScreen.handleRestore` fakes the IAP locally with no receipt validation). Both are App Store reject risks.
- **2 apps are in categories commoditized to $0 in 2026.** Fraus (free T-Mo/Verizon/iOS 26/Norton-in-ChatGPT) and Salvis (Medisafe went paid at $4.99 Jan 1; Salvis at $7.99 is 60% above the leader).
- **Portfolio plan's $5K/mo-by-month-6 target is not supported by cross-review evidence.** Realistic combined: $1.5-2K by month 6, $3-5K by month 12 IF Patet B2B Certified™ pilot clicks.

---

## Verdict matrix

| App | Func | Sell | Verdict | Realistic 12-mo MRR | Critical defect found |
|---|---|---|---|---|---|
| **Patet** | B | C+ | Ship with 2 gate fixes | $850 (B2B upside $1.5-3K) | Dev tier-cycle Pressable in prod build (FIXED), Render Blueprint never imported |
| **Vinla** | B- | D+ | Blocked on real IAP | $150-450 | Fake IAP in `PaywallScreen.tsx:65-73`, `BETA_PRO_ACCESS=true` Sonnet bleed, no 18+ gate |
| **Winlet** | B- | D+ | Distribution-blocked, not product-blocked | $180 (B2B Slack upside $500+) | `BETA_PRO_ACCESS=true`, no token revocation, `[Your State]` placeholder, web parity gaps |
| **Glyphe** | A- | D | Blocked on distribution + tier UI | $400-900 (B2B schools upside $2.5-4K) | `lib/tier.ts` has identical feature lists across all 3 tiers; upgrade CTA fires "Coming Soon" |
| **ClearDoc** | B | D | Shelve unless medical-bills pivot + free + annual + dispute letter | $300-700 post-pivot | Anonymous-auth orphans history; 1-scan trial dies on first blurry photo; no dispute PDF export |
| **SitterSheet** | A- | C- | Ship as-is, low effort | $40-120 | Mis-categorized in portfolio plan — is pet/house sitter handoff, NOT babysitter |
| **Fraus** | C+ | D | Depends on CPL; lean shelve | Sub-$200 consumer-only | $50 budget yields 1-2 leads at $27-42 healthcare 55+ CPL — statistically meaningless |
| **Salvis** | C | D+ | Shelve OR B2B pivot to pharmacy/AL facilities | $250-700 consumer; $1-3K B2B | Voice-first claim is 100% landing copy — no voice infrastructure built; pricing 60% above paid leader |

---

## Cross-cutting patterns

### 1. The consumer-only ceilings are real, and lower than the portfolio plan assumed

Reviewers independently arrived at sub-$1K consumer ceilings for 5 of 8 apps. The portfolio plan (`~/.claude/plans/swift-wobbling-crystal.md`) projected $7,300-20,700 combined by month 12. After review, the realistic floor-to-realistic span is **$1,800-3,500 by month 12** without B2B layers landing.

### 2. B2B pivots are the only $1K+ MRR path for the apps that have one

| App | B2B angle (reviewer-surfaced) | Validation comp |
|---|---|---|
| Patet | B2B2C Certified™ license to credit unions / community colleges | Zogo (acquired by Nymbus 2025) |
| Winlet | Slack/Teams Wins Board team subscriptions | Matter ($1-3/seat), Bonusly ($3+/seat) |
| Glyphe | School / youth-org licensing | Headspace Ebb bundled into 2,000+ employer mental-health packages |
| Salvis | Independent-pharmacy white-label + AL facility ops tools | Med-mgmt SaaS $9.11B → $23.29B by 2030 |
| Fraus | RIA / senior-living facility white-label | LifeLock/Aura partnerships |

The first 4 share a pattern: **one $200-500/mo B2B customer = same revenue as 67-170 consumer subs at $2.99/mo, with lower CAC and lower churn.** A pivot motion (cold outreach + Loom demos + pilot pricing) replaces a paid-acquisition motion the $50/app budget can't fund.

### 3. Multiple apps have working code but broken revenue paths

- **Glyphe:** 718 tests, hardened crisis detection, A-grade code — but the upgrade CTA fires `Alert.alert('Coming Soon')` and `lib/tier.ts` ships identical feature lists across Free/Daily/Deep. The upgrade screen literally shows a table with checkmarks in every cell.
- **Vinla:** Custom JWT + Neon, server-side cost guard, atomic limits — but `PaywallScreen.handleRestore` calls `upgradeToProPlus()` locally with no receipt validation. App Review will reject.
- **Patet:** Now fixed — Dev tier-cycle Pressable was visible in prod builds (commit `312e7ce`).

The pattern: solo-dev sprints prioritized features over monetization plumbing. Every app needs an end-to-end IAP smoke before any of them ship.

### 4. The portfolio's pre-existing memory had several stale or wrong facts

- **SitterSheet is a pet/house sitter handoff tool**, not a babysitter app. Real competitor is `caresheet.app` ($1.99/mo or $19.99 lifetime). The "NYC SitterSheet babysitter competitor" flagged in the portfolio plan as a TM/ASO risk **did not surface in 2026 search** — may be defunct.
- **Vinla is already on custom JWT + Neon Postgres**, migrated 2026-04-20. The `project_vinla_todo.md` "client-side tier (CRITICAL)" and "RLS missing (CRITICAL)" pre-launch blockers are misstated — cost guard is server-side and atomic; health data is on-device. Memory needs correction.
- **ClearDoc already ships `cleardoc_pack20` at $4.99 + `cleardoc_monthly` at $7.99/mo with 1 free scan** — not "$7.99 monthly-only" as the portfolio plan stated. But there's still no annual SKU and the roadmap defers it 3 months. Reviewer says ship annual at launch.
- **Glyphe's 12-q personality quiz is weaker than memory implies** — it asks the user to give advice on 12 scenarios, not to describe themselves. ChatGPT GPT-5.5 ships 6 personality presets + memory sources on every tier including free. The "personality calibration moat" is thinner than the project memory describes.

### 5. 2026 market intel the portfolio plan didn't anticipate

| Date | Event | Affects |
|---|---|---|
| 2026-01-01 | Medisafe moved to paid at $4.99/mo | Salvis pricing now 60% above category leader |
| 2026-01-01 | CA SB 243 effective ($1k+/violation + private right of action on AI companion law); NY $15k/day AI companion law; federal GUARD Act | Glyphe at 16-27 target is regulatory landmine |
| 2026-01 | Character.AI banned under-18s after settled teen-suicide suits | Glyphe must re-target 18-24 with hard age gate |
| 2026-02-18 | AT&T ActiveArmor raised paid tier $3.99 → $7/mo with $1M ID fraud reimbursement | Fraus's $4.99 sits below the new bundled-protection baseline |
| 2026-03-02 | Cal AI acquired by MyFitnessPal at ~$50M ARR | Vinla "AI food photo" wedge is closed |
| 2026-03-04 | Norton Genie absorbed into ChatGPT | Fraus consumer AI scam detection now free in ChatGPT |
| 2026-04-21 | Monarch Money launched $199/yr Plus tier | Mid-market budget app pricing keeps climbing |
| 2026-05-17 | OpenAI launched ChatGPT + Plaid integration | Same day Patet's Plaid creds landed — "AI reads your bank" is no longer a moat |

The portfolio plan was written before all 8 of these. **Patet's defensible angle pivots from "AI reads your bank" to "curriculum + Certified™ + LATAM Spanish + sub-$3 price."**

---

## Memory corrections to land

After this synthesis is reviewed:

1. **`project_app_renames.md` + `swift-wobbling-crystal.md`:** SitterSheet is pet/house sitter, not babysitter. Real competitor is CareSheet.app. NYC competitor flagged for TM/ASO conflict may not exist.
2. **`project_vinla_todo.md`:** Stack is custom JWT + Neon Postgres (migrated 2026-04-20), NOT Supabase Auth + SQLite. Cost guard is server-side and atomic. RLS issue is irrelevant (health data on-device). The "CRITICAL" pre-launch blockers list needs rewriting against current code.
3. **`project_portfolio_pricing.md` or new memory:** ClearDoc already has `cleardoc_pack20` $4.99 + `cleardoc_monthly` $7.99 with 1 free scan. Annual SKU still missing and should ship at launch, not in 3 months.
4. **`swift-wobbling-crystal.md` portfolio MRR projection:** $5K/mo by month 6 not supported by review evidence. Realistic: $1.5-2K month 6, $3-5K month 12 only if Patet B2B Certified™ lands a pilot.

---

## Ranked next actions (cross-portfolio)

Ordered by ROI per dev-hour, with effort estimates.

| # | Action | App | Effort | Expected lift |
|---|---|---|---|---|
| 1 | Import `render.yaml` Blueprint via Render dashboard | Patet | 5 min HUMAN | Activates Sunday Money Wrapped + onboarding email crons (currently silent no-ops in prod) |
| 2 | Flip `BETA_PRO_ACCESS = false` server+client | Vinla, Winlet | 1 hr each | Stops Sonnet bleed; activates real tier gates |
| 3 | Fix Glyphe `lib/tier.ts` to ship real differentiated feature lists + remove "Coming Soon" Alert | Glyphe | 1 day | Makes the existing paywall actually functional |
| 4 | Real IAP integration in Vinla `PaywallScreen` (replace local fake) | Vinla | 2-3 days | App Review unblock |
| 5 | Patet B2B Certified™ outreach: pre-write one-pager + Loom + cold-email batch to NACFC + community college foundations | Patet | 2 days | $1.2-2.4K MRR from one pilot per reviewer |
| 6 | Winlet B2B Slack Wins Board MVP (mount existing routes + Slack app + simple per-seat pricing page) | Winlet | 5-7 days | $180+/mo per team |
| 7 | ClearDoc medical-bills pivot decision: rename + free tier + annual + dispute letter export, OR shelve | ClearDoc | 2-3 weeks if pursued | $300-700/mo realistic |
| 8 | Fraus + Salvis: run the $50 validation ads BEFORE more code; honor the kill thresholds | Fraus, Salvis | $100 total spend | Confirms shelve or B2B-only path |
| 9 | SitterSheet: ship as-is at $1.99 lifetime (per reviewer reco mirroring CareSheet) | SitterSheet | 1 day | $40-120/mo upside |

Steps 1-4 are the launch unblockers. Step 5 is the highest-MRR single move in the portfolio. Steps 7-8 settle whether to keep investing in those four apps at all.

---

## Recommended portfolio reframing

The original portfolio plan treated all 8 apps as parallel revenue bets at roughly similar weight. The reviews collectively suggest a different structure:

- **Tier 1 (real revenue contenders, both with B2B layers):** Patet, Winlet
- **Tier 2 (functional but distribution-blocked; B2B pivot might rescue):** Glyphe (only after regulatory + tier-UI fixes), Vinla (only after real IAP)
- **Tier 3 (validation-gated; treat as $100 experiments):** Fraus, Salvis
- **Tier 4 (low-effort harvests, accept ceiling):** SitterSheet ($40-120/mo as-is)
- **Tier 5 (decide whether to pivot or shelve):** ClearDoc

This reframing matters because the $5K-by-month-6 target was driving spread-thin effort across all 8. The reviews say: **concentrate Tier 1 (Patet B2B + Winlet B2B) and stop investing real dev time in Tier 3-5 until they prove they deserve more.**
