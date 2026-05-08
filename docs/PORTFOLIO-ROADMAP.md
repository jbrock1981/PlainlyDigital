# Plainly Digital LLC — Portfolio Roadmap

**Last updated:** 2026-04-17
**Owner:** Jonathan Brock
**Partner doc:** `../Plainly_Digital_Master_Tracker.md` (canonical per-product status)

This roadmap shows **what's next across the portfolio**, grouped by horizon. It complements (does not replace) the master tracker.

---

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
- [ ] Apple Developer account ($99/yr) — unblocks all four core apps for App Store submission
- [ ] RevenueCat integration across apps with paid tiers
- [ ] Configure Plainly server env vars on Render (Plaid, Google OAuth, internal API key)
- [ ] Plainly audit C1/C2/C3 (test suite regression; Plaid revocation on delete; pdf-parse crash)
- [ ] Vinla audit C1/C2/C3 (server-side prompt assembly; Sonnet tier enforcement; cost-guard race)
- [ ] Winlet audit C1/C2 (cost-guard race; timing-safe webhook)
- [ ] Notch Privacy Policy + ToS
- [ ] Notch DBA registration under Plainly Digital LLC

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
- [ ] Notch invite beta → public beta
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
- Every AI-backed feature must go through Notch 3-layer architecture + NIST AI RMF docs (see `NOTCH-BRAND-PERSONALITY.md`, `NIST-AI-GOVERNANCE.md`)
- No Supabase auth on new apps — custom JWT per the Winlet pattern (portfolio decision locked 2026-04-17)
- Google + Apple sign-in added only **after** email/password MVP is live in App Store + Play Store
- USPTO intent-to-use filings before public ad spend on any new brand

---

## Cross-product decisions locked 2026-04-17

- **Auth:** No Supabase. Custom JWT following the Winlet pattern for every new app.
- **Name clearance:** Always check iOS App Store, Play Store, and USPTO before committing to a new brand. Two names were rejected at scaffolding (ScamShield → Fraus; Pill Buddy → Salvis).
- **Validate-then-build:** For any new consumer app, ship landing + Meta Pixel first, validate CPL against published thresholds, only then commit 2–4 weeks to an MVP.
