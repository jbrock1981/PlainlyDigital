# Plainly Digital LLC — Portfolio Roadmap

**Last updated:** 2026-05-11
**Owner:** Jonathan Brock
**Partner doc:** `master-tracker.md` (canonical per-product status) + `PORTFOLIO-LAUNCH-CHECKLIST.md` (operational ticks)

This roadmap shows **what's next across the portfolio**, grouped by horizon. It complements (does not replace) the master tracker.

---

## Recent (2026-05-11)

- **Patet Spanish lesson content shipped** (machine-translated via Sonnet 4.6 — 121 lessons across 18 modules + 11 supporting surfaces). Native LATAM reviewer pass remains the open thread before commercial Latam launch.
- **Patet monetization Phase 1: persona packs + feature unlocks tied to lessons** (server unlocks lib + migration 019 `users.coach_persona` + LockedFeatureGate + PersonaSwitcher).
- **Patet monetization Phase 2: \$19 Patet Certified™ paid credential** (migration 020 + RC `patet_certified_credential` IAP + vanity slug + LinkedIn Add-to-Profile).
- **Brand rename Notch → Glyphe across 5 repos** (Patet, PlainlyDigital, Vinla, Winlet, Glyphe app) after 10bit FX TM block. Glyphe clearance pass still pending.
- **Neon migrations 010-017 + 019 + 020 caught up against `royal-lake-78408653` "plainly" project** (production DB had drifted behind the codebase; resolved 2026-05-11 evening).

## Now (next 2 weeks)

### Quick-revenue validation track — Fraus + Salvis
Shipped landing-page scaffolds 2026-04-17. Owner must execute the validation gate before any MVP work.

- [ ] Create Neon project (separate) for Fraus and Salvis
- [ ] Create Meta Pixels (separate) for each
- [ ] Purchase `<your fraus domain>` and `<your salvis domain>`
- [ ] File USPTO intent-to-use ($350 each)
- [ ] `npx vercel --prod` for each repo
- [ ] Fraus: $50 / 48hr Meta ad set targeting 55+, "concerned about scams" + "caregiver" interests
- [ ] Salvis: $50 / 48hr Meta ad set A (60+, "medication management") + ad set B (40–55, "caring for aging parent")
- [ ] **Green-light gate:** Fraus CPL < $3; Salvis CPL < $4
- [ ] **Reposition gate:** Fraus CPL > $8; Salvis CPL > $10

### Core four — production readiness
- [ ] Apple Developer account ($99/yr) — unblocks all four core apps for App Store submission (funded — pending the account creation step)
- [x] RevenueCat integration across apps with paid tiers (Patet shipped — 7 IAPs incl. patet_certified_credential)
- [ ] Configure Patet server env vars on Render (Plaid prod, Google OAuth, internal API key, RevenueCat webhook auth, PATET_LINKEDIN_ORG_ID)
- [ ] **Patet Plaid production meeting 2026-05-12.** See `PORTFOLIO-LAUNCH-CHECKLIST.md` Plaid setup block — confirm Auth product NOT in scope (read-only Transactions/Recurring/Balance only); InfoSec policy upload (NOT YET WRITTEN — TODO scaffold).
- [x] Patet audit closures landed (data export, PII encryption, JWT cookie, persistent token revocation, OG image, persona unlocks, paid credential)
- [ ] Vinla audit C1/C2/C3 (server-side prompt assembly; Sonnet tier enforcement; cost-guard race)
- [ ] Winlet audit C1/C2 (cost-guard race; timing-safe webhook)
- [ ] Glyphe USPTO + App Store + Play + .com clearance pass (replaces blocked "Notch"; not yet cleared)
- [ ] Glyphe Privacy Policy + ToS
- [ ] Glyphe DBA registration under Plainly Digital LLC (post-clearance)

### Monetization Phase 3 (next, ~6 weeks)
- [ ] Gift subscriptions (Patet) — `patet_gift_pro_annual` $24.99 + `patet_gift_proplus_annual` $57.99 RC non-consumables; buy + redeem flows; `gift_codes` migration; distribution via r/personalfinance, parent FB groups, grad round-ups
- [ ] Money Wrapped share card (monetization phase 4 — month-end push + IG/TikTok/Twitter share targets)
- [ ] Affiliate partner expansion (Policygenius, Lemonade, Public, Robinhood, Cash App Taxes, Keeper Tax, Credit Karma, Experian, Stripe Atlas, Doola)
- [ ] Premium content packs ($4.99 one-time IAPs: Side Hustle Stack, First Apartment, Wedding Money, New Grad Starter Kit, Crush Student Loans)
- [ ] B2B outreach: 50 high schools / 20 credit unions / 10 universities (90-day pilot offer)

---

## Next (4–8 weeks)

### Fraus / Salvis MVPs — CONDITIONAL on validation gate
If validation greenlights, mirror the Winlet stack:
- Express + TypeScript + JWT (custom auth — no Supabase) on Render
- Neon Postgres
- Claude API with `cost-guard.ts` tier enforcement
- Expo React Native mobile (voice-first for Salvis; paste/OCR-first for Fraus)
- RevenueCat for payments
- Apple + Google sign-in added **after** first successful App Store + Play Store listings

Salvis adds two hard legal gates before public launch:
- [ ] HIPAA review (family sharing creates covered-entity risk surface)
- [ ] Apple medical-app guideline review (app must never recommend dosages)

### Core four — public beta
- [ ] Plainly public beta
- [ ] Vinla public beta (requires Supabase sync + age gate)
- [ ] Glyphe invite beta → public beta
- [ ] Winlet domain purchase (<your winlet domain>) + App Store submission

---

## Later (3–6 months)

- [ ] App Store + Play Store submissions across all shipping apps
- [ ] Marketing / ASO strategy portfolio-wide
- [ ] Fraus + Salvis domain + trademark lock-in (contingent on validation)
- [ ] Evaluate graduating repos into a PlainlyDigital GitHub Organization
- [ ] Consider bundling Fraus + Salvis into a single "Fraus Plus" family-safety subscription if both validate (share the family-plan back end)

---

## Standing gates (portfolio-wide)

- Every customer-facing app must have ToS + Privacy Policy before public launch
- Every AI-backed feature must go through Glyphe 3-layer architecture + NIST AI RMF docs (see `docs/GLYPHE-BRAND-PERSONALITY.md` in this repo + `Patet/docs/NIST-AI-GOVERNANCE.md`)
- Persona overlays + crisis-safety + product-disclosure rules are NEVER stripped by any persona switch (locked invariant in `Patet/server/src/lib/system-prompt.ts`)
- No Supabase auth on new apps — custom JWT per the Winlet pattern (portfolio decision locked 2026-04-17)
- Google + Apple sign-in added only **after** email/password MVP is live in App Store + Play Store
- USPTO intent-to-use filings before public ad spend on any new brand

---

## Cross-product decisions locked 2026-04-17

- **Auth:** No Supabase. Custom JWT following the Winlet pattern for every new app.
- **Name clearance:** Always check iOS App Store, Play Store, and USPTO before committing to a new brand. Two names were rejected at scaffolding (ScamShield → Fraus; Pill Buddy → Salvis).
- **Validate-then-build:** For any new consumer app, ship landing + Meta Pixel first, validate CPL against published thresholds, only then commit 2–4 weeks to an MVP.
