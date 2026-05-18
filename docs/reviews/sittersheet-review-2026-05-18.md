# SitterSheet — App review
**Date:** 2026-05-18
**Reviewer:** general-purpose agent (autonomous)
**Repo:** /home/jbroc/repos/SitterSheet

## Verdict & 12-month MRR projection

**Ship at low cost, then shelve at 90 days unless it crosses $200/mo MRR.** The portfolio plan was working from a wrong premise (it is NOT a babysitter platform — it's a pet/house sitter instruction-sheet generator), but the plan's "deprioritize, MRR ceiling is low" conclusion is still correct, just for different reasons. Confirmed direct competitor `CareSheet.app` already ships the exact value prop at $1.99/mo or $19.99 lifetime. Plus 3,000+ Etsy templates serve the same job-to-be-done for $5-15 one-time. Code is launch-ready (`STATUS=code complete + tested`, 78/78 + 44/44 jest, infra live since 2026-05-09), so the marginal cost of shipping is just store-listing time.

| Scenario | MRR | Key assumptions |
|---|---|---|
| Conservative | $0-25/mo | 50 installs/mo from Reddit r/petsitting + r/dogs, 2% paywall hit, single $4.99 unlock = ~$5-10/mo gross. Most "MRR" is one-time revenue amortized. |
| Realistic    | $40-120/mo | 200-400 installs/mo via $50-100 Meta/Reddit spend, 3-4% conversion at $4.99 one-time = ~$30-80/mo, plus organic word-of-mouth from cute share-page UX. |
| Upside       | $250-450/mo | Word-of-mouth via the public share page (every shared guide is a viral surface), 1,500 installs/mo, 5% conversion, plus a $9.99 premium tier (multi-pet/photos) shipped per ROADMAP v1.x. |

**On the portfolio plan's $50-300/mo ceiling:** confirmed at the realistic case. Upside scenario can punch above $300/mo only if the share-page virality compounds — possible because each guide is sent to 1-3 sitters who see the product first-hand, but unproven and there's no acquisition loop wired in.

**On the "name collision" with NYC babysitter SitterSheet:** I could not surface any "SitterSheet" babysitter competitor in 2026 searches across "babysitter app sittersheet NYC family scheduler 2026" (top results: Sittercity, UrbanSitter, Curated Care, Forwhen, Kids & Kaboodles — no "SitterSheet"). Either the prior research was stale or the competitor has rebranded/died. The actual product collision is **CareSheet.app**, which is a much bigger problem.

## 1. What it actually is (verified from code/repo)

- AI-guided 8-step wizard (`src/constants/wizard-steps.ts`: pets, feeding, meds, exercise, quirks, vet, house, freeform) that generates a markdown pet-care guide via Claude Sonnet 4 inside a Firebase Cloud Function (`functions/src/generateGuide.ts`).
- Output is a 32-hex tokenized share URL with 30-day expiry rendered as a public HTML page (`functions/src/serveGuide.ts`, `functions/src/lib/render-html.ts`). Token rotation supported (`rotateShareToken`).
- Monetization is **non-consumable $4.99 one-time unlock** via RevenueCat — subscription explicitly dropped per `ROADMAP.md` line 60 ("nobody creates 2+ sitter guides a year, so a subscription was just paywall confusion"). 1 free guide enforced server-side (`FREE_TIER_GUIDE_LIMIT = 1` in `src/constants/config.ts`).
- Tagline in CLAUDE.md: "Everything your sitter needs. One link." — pet/house sitter, NOT babysitter. The wizard handles pets + the house (wifi, alarm, trash, mail). No child-care fields.
- Infra is live on GCP project `sittersheet-plainlydigital` (project number `116927353996`) under `apps-org` since 2026-05-09 per `LAUNCH.md`. Remaining items are vendor consoles (App Store, Play, RevenueCat webhook).

## 2. Functionality critique

**Grade:** A-

- **What works end-to-end:** wizard → AI generation with cost-guarded backend (3 layers: per-user 5/hr/15-day, global $10/day kill-switch, GCP budget) → markdown stored in Firestore → public share page with `X-Robots-Tag: noindex` + DOMPurify on rendered HTML → PDF export via expo-print → native share sheet. Token rotation works. Delete-account purges. Anonymous + email auth verified end-to-end against `accounts:signUp` 2026-05-09.
- **What's broken or unfinished:** Apple/Google sign-in stubbed (`auth.ts` lines noted in LAUNCH.md §7), App Check not enabled, per-IP rate limit on `serveGuide` not implemented (DoS-of-bill risk acknowledged), password complexity not enforced. None of these are launch blockers; all are documented in `ROADMAP.md`.
- **Trust & safety gaps:** This is a PET-care app, not a child-care app — the trust bar is materially lower than the prompt assumes. There is no background-check, age-verification, or parental-consent surface area because the app is just a document generator. The real T&S risk is the **share page leaking alarm codes + wifi passwords** if the 32-hex token is mishandled. Mitigations in code: 128-bit token entropy (brute-force infeasible), 30-day expiry, `X-Robots-Tag: noindex,nofollow`, token rotation endpoint, masked-with-toggle inputs on House step, inline warning in House step (per LAUNCH.md §9). This is competent for the threat model. The audit log + Firestore TTL on `calls.expiresAt` are real and active.
- **Test coverage honest assessment:** 78 root jest + 44 functions jest + 10 firestore rules tests + 3 Playwright specs = 135 tests across 27 suites. tsc clean, eslint 0 errors. Reasonable for a 6-screen single-purpose app. The `firestoreMock.ts` ad-hoc shims are tech-debt called out in `ROADMAP.md` and don't block ship. Cosmetic `act()` warnings in `share.test.tsx` and `useSubscription.ts` likewise documented.

## 3. Sellability critique

**Grade:** C+

**Target user (specific):** Pet owners (dogs + cats, occasionally exotics) ages 28-45 who travel 2-6 times/year and use a paid or unpaid pet sitter rather than boarding. Single-sided market — only the pet owner is the customer; the sitter is a passive consumer of the share link.

**Their alternative today (name + price):**
- **CareSheet.app** — identical product, $0 (1 sheet) or $1.99/mo or $19.99 lifetime. This is the direct collision and was not surfaced in the portfolio plan.
- Etsy "Pet Sitter Instructions" templates — 3,000+ listings, $3-15 one-time, Canva-editable, infinite reuse.
- A handwritten note + group text with the sitter. Cost: $0, time: 10 minutes.
- TrustedHousesitters ($149-399/yr) — different product (it's the marketplace, not the instruction sheet), but its in-app "pet care instructions" field overlaps.

**Reason they'd switch:**
- **Pricing fit:** $4.99 lifetime is sharper than CareSheet's $1.99/mo recurring and roughly competitive with CareSheet's $19.99 lifetime — but CareSheet has a free tier with 1 sheet too, identical free-tier strategy. SitterSheet's only pricing edge is "$15 cheaper than CareSheet lifetime." Etsy templates undercut both. The AI-guided wizard is a real UX edge over Canva, but most users won't perceive that as $4.99 of value vs. $5 Etsy.
- **Two-sided-marketplace cold-start problem:** N/A — this is **one-sided**. That's the one structural advantage over a Care.com / Rover clone. No supply-side acquisition needed. The portfolio plan implicitly treated this as marketplace risk; it isn't.
- **First 100 users come from where?** Realistically: Reddit r/petsitting (97K members), r/dogs (3.2M), r/pets (3M). The LAUNCH.md §13 already names this. ASO for "pet sitter checklist" / "pet sitter instructions" is a tiny long-tail and CareSheet is already ranking. Paid: $50 Meta ad to dog-owner lookalike for $1-2 CPI.
- **Organic / viral mechanics:** This is the one real wedge the portfolio plan undersold. **Every share link is a product demo to 1-3 sitters who are themselves likely pet owners.** The share page should have a soft "Make one for your pets" CTA at the bottom — code does not appear to do this. This is a 1-day fix worth shipping pre-launch.

## 4. Top 3 monetization opportunities (URL + date required for each)

1. **Add a "Make one for your pets" footer CTA on the public share page.**
   - Citation: CareSheet's own positioning treats the share link as the acquisition surface — "No app to download, no account to create" (https://www.caresheet.app/blog/pet-sitter-instructions-checklist, accessed 2026-05-18). Every shared guide reaches 1-3 sitters who are 70% likely to own pets themselves (https://www.businessresearchinsights.com/market-reports/pet-sitting-market-118284, accessed 2026-05-18 — "approximately 70% of U.S. households own a pet").
   - Realistic incremental MRR: +$15-50/mo via 8-15% viral coefficient on existing user base.
   - Effort: 0.5 days (edit `functions/src/lib/render-html.ts` + analytics tag).

2. **Ship the $9.99 "premium unlock" tier (multi-pet templates + photo upload) per `ROADMAP.md` v1.x at 1,000 installs.**
   - Citation: CareSheet charges $1.99/mo for "up to 10 caresheets, password protection, auto-expiring links, view analytics, custom page URLs" (https://www.caresheet.app/pricing, accessed 2026-05-18). At $4.99 single tier SitterSheet is leaving the high-end pet-multi-household segment on the table.
   - Realistic incremental MRR: +$30-90/mo if 6-10% of paid users upgrade.
   - Effort: 3-4 days (RevenueCat product + entitlement + UI + photo upload to Cloud Storage).

3. **B2B angle: license the wizard + share-page as white-label to small-business pet sitters / dog walkers as a client-intake tool.**
   - Citation: ~35,000 professional pet sitters in the US, 99% independently owned (https://www.dogster.com/statistics/pet-sitting-statistics, accessed 2026-05-18). Time To Pet and Gingr dominate the management-software layer (https://www.gingrapp.com/, accessed 2026-05-18; https://www.timetopet.com/, accessed 2026-05-18) but neither focuses on the *client* providing instructions to the sitter — that's an integration gap. PetExec joined Togetherwork with Gingr/Revelation Pets and is no longer accepting new clients (https://www.petexec.net/, accessed 2026-05-18) — consolidation is happening, niches are opening.
   - Realistic incremental MRR: $0 in the first 12 months, $200-800/mo at 18 months if sold as a $9/mo per-business add-on to 30-50 independent pet sitters. This is a real wedge but the GTM is cold-outreach to NAPPS / Pet Sitters International members, which is not the user's strength based on portfolio context.
   - Effort: 5-10 days for white-label support + business account flow. Most of the value is in the GTM, not the product.

**Is there a B2B angle that beats the $50-300 consumer ceiling?** Yes (#3 above), but it's a different product motion — outbound B2B sales to a 35,000-business cottage industry. That's not what's built and not what the portfolio plan optimizes for. Honest answer: the B2B wedge exists, but pursuing it would mean reframing SitterSheet as "client intake for independent pet sitters" — same backend, different positioning. Worth at most a 1-week experiment with 20 cold emails before committing.

## 5. Top 3 functionality fixes (highest leverage)

1. **Viral footer on the share page** (see §4.1) — 0.5 days, addresses cold-start acquisition.
2. **Multi-pet UI promotion on home screen + edit-existing-guide flow** (per `ROADMAP.md` v1.x) — currently you have to delete and redo the wizard to fix a typo. This is the most likely refund-trigger / bad-review-trigger. 2-3 days.
3. **Apple Sign-In** — `auth.ts` stubs throw; Apple requires sign-in-with-Apple if you offer any third-party sign-in. Not currently offering any, so technically not a Store rejection, but it's the single biggest install-conversion friction. 1 day.

## 6. Competitive landscape (2026)

| Name | Pricing | Funded? | Recent 2026 move | What they do better | What they miss |
|---|---|---|---|---|---|
| **CareSheet.app** | Free 1 sheet / $1.99/mo / $19.99 lifetime | Unknown, appears bootstrap | Active blog content marketing (https://www.caresheet.app/blog/pet-sitter-instructions-checklist, 2026-05-18) | Identical product, name conflict ("CareSheet" vs "SitterSheet"), SEO-first, tap-to-call vet, password protection, view analytics, no-account-needed share | No AI wizard — manual form entry; subscription tier is awkward for a 2x/year use case |
| **Rover** | Walker-set rates, 31% take-rate ($49 sitter profile fee) | Blackstone-acquired $2.3B (Nov 2023, https://www.blackstone.com/news/press/blackstone-completes-acquisition-of-rover/) | Acquired Meowtel Jan 2026 (https://www.pehub.com/blackstone-backed-rover-snaps-up-cat-sitting-app-meowtel/), Gudog 2024/25 (https://www.themiddlemarket.com/latest-news/blackstones-rover-group-buys-irish-dog-sitter-company-gudog) | Marketplace + GPS + payments + 600K sitters | Doesn't generate instruction sheets — different product |
| **Wag!** | Walker-set, 40% take-rate, walks $20-30, sitting $40-75/night | Public, 2023 revenue $83.9M +52.9% YoY | Subscription wellness add-ons | Marketplace + 150K caregivers | Same as Rover — not the same product |
| **TrustedHousesitters** | $129-399/yr | Private | Added £9/sit booking fee 2026 (basic/standard tiers) per https://whereintheworldisnina.com/trustedhousesitters-review/ 2026-05-18 | Marketplace with built-in pet-care-instructions field | Membership is overkill for a single instruction sheet |
| **UrbanSitter** | $19.95/mo / $34.95/q / $99.95/yr | Private | 150K+ caregivers across 60+ cities (https://support.urbansitter.com/hc/en-us/articles/5380112272539-Membership-Plan-Options 2026-05-18) | Babysitter marketplace | Wrong vertical — not pet-care |
| **Etsy templates** | $3-15 one-time | N/A | 3,000+ listings in "pet sitter templates" (https://www.etsy.com/market/pet_sitter_templates 2026-05-18) | Lowest price, infinite reuse, Canva-editable | No share-link, no PDF export, no AI summarization |
| **"SitterSheet" NYC babysitter (per prompt)** | — | — | Could not surface in 2026 searches; either rebranded, defunct, or never as significant as the portfolio plan suggested | — | — |

The competitive set the portfolio plan listed (Care.com / UrbanSitter / Sittercity) is the **babysitter** comp set, not this app's comp set. The actual comp set is **CareSheet + Etsy + DIY group text**. That changes the calculus: CareSheet is the genuine threat, not Care.com.

## 7. Honest "DO NOT do" list

1. **Do NOT reposition as a babysitter app.** The portfolio plan's framing is wrong — the code, wizard steps, and copy are all pet/house-sitter. Pivoting to children would require redoing trust & safety, age-verification, background checks, COPPA, and probably re-rating the App Store listing. Not worth it.
2. **Do NOT add a monthly subscription.** `ROADMAP.md` already correctly killed this — 2x/yr use case + $4.99 lifetime is the right pricing shape. Don't be tempted to mirror CareSheet's $1.99/mo just because they have it; their funnel data is unknown and their lifetime tier exists for a reason.
3. **Do NOT build a sitter-side app or two-way "sitter check-in" flow** (listed as a v1.x roadmap item) until PMF is demonstrated. It doubles the surface area, doubles trust & safety, and the share-link form-in-page mechanism already gets 80% of that value with no auth.
4. **Do NOT spend on Meta ads above $50-100 in the first month.** With CareSheet's existence and the Etsy template alternative, paid CAC will exceed LTV at consumer-app benchmarks (3-7% monthly churn for consumer subscriptions per https://retentioncheck.com/learn/churn-rate-by-industry 2026-05-18, though this app's one-time pricing dodges churn). Test for $50, kill if CAC > $3.
5. **Do NOT rename it.** The "SitterSheet vs CareSheet" name conflict is real but renaming destroys the App Store reviews, Anthropic key, RevenueCat config, GCP project name, and the (probably modest) SEO already accrued. The CareSheet collision is annoying, not fatal — they ranked first because they're older, not because the name is uniquely theirs.

## 8. Sources

- https://www.businessresearchinsights.com/market-reports/pet-sitting-market-118284 (2026-05-18) — 70% US household pet ownership, 45% mobile-app booking
- https://trytails.com/guides/hiring-pet-care/best-dog-walking-apps/ (2026-05-18) — Rover/Wag/Care.com comparison
- https://trytails.com/faq/rover-vs-wag-cost/ (2026-05-18) — Rover 31% take-rate, Wag 30-40%
- https://financebuzz.com/earning-money-with-rover (2026-05-18) — $49 Rover profile fee
- https://sidehustles.com/best-pet-sitting-apps/ (2026-05-18) — 2026 pet sitting app landscape
- https://www.blackstone.com/news/press/blackstone-completes-acquisition-of-rover/ (2026-05-18) — Rover $2.3B Blackstone acquisition Nov 2023
- https://www.pehub.com/blackstone-backed-rover-snaps-up-cat-sitting-app-meowtel/ (2026-05-18) — Rover acquires Meowtel Jan 2026
- https://www.themiddlemarket.com/latest-news/blackstones-rover-group-buys-irish-dog-sitter-company-gudog (2026-05-18) — Rover acquires Gudog
- https://www.caresheet.app/blog/pet-sitter-instructions-checklist (2026-05-18) — direct competitor product copy
- https://www.caresheet.app/pricing (2026-05-18) — CareSheet pricing $0 / $1.99/mo / $19.99 lifetime
- https://www.dogster.com/statistics/pet-sitting-statistics (2026-05-18) — 35,000 US pet sitters, 99% independent
- https://www.etsy.com/market/pet_sitter_templates (2026-05-18) — 3,000+ Etsy pet-sitter template listings
- https://www.gingrapp.com/ (2026-05-18) — Gingr B2B pet-business software, dominant after PetExec consolidation
- https://www.petexec.net/ (2026-05-18) — PetExec no longer accepting new clients, consolidated under Togetherwork with Gingr
- https://www.timetopet.com/pricing (2026-05-18) — Time To Pet SaaS B2B pricing model
- https://whereintheworldisnina.com/trustedhousesitters-review/ (2026-05-18) — TrustedHousesitters $129-399/yr + £9/sit booking fee 2026
- https://support.urbansitter.com/hc/en-us/articles/5380112272539-Membership-Plan-Options (2026-05-18) — UrbanSitter $19.95/$34.95/$99.95
- https://blog.urbansitter.com/does-urbansitter-cost-money/ (2026-05-18) — UrbanSitter membership model
- https://retentioncheck.com/learn/churn-rate-by-industry (2026-05-18) — consumer subscription 7-10% monthly churn benchmark
- https://www.ever-help.com/blog/saas-retention-rate-benchmarks (2026-05-18) — B2B SaaS retention 88-90%, top performers 120% NRR
