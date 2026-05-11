# Plainly Digital LLC — Portfolio Launch Checklist

Created: 2026-05-11 (last updated 2026-05-11 evening — Phase 1+2 monetization landed)
Scope: actions you (the human) need to complete. Cross-app, ranked by leverage. Code-side work tracked separately in each app's CLAUDE.md.

---

## Plaid setup — meeting tomorrow morning (2026-05-12)

You're mid-flow on the Plaid production application. Items surfaced during setup:

- [ ] **Confirm product scope on submission.** Originally Transactions + Recurring Transactions + Balance. **Auth** (bank account/routing numbers, ACH) was mentioned later but was NOT in the original scope — only enable it if Patet actually needs ACH money-movement, which today it doesn't. Keep read-only.
- [ ] **InfoSec Policy upload.** Plaid asks: "Does your organization have a documented information security policy and procedures…?" — **you do NOT have one ready today.** Either answer "No" (escalates to manual review) or pause the form and have me scaffold a 5-page Plainly Digital ISMS doc (you already operationalize most of it — Helmet/CORS, AES-256-GCM PII encryption, JWT revocation, account lockout, audit logging, NIST AI RMF docs — so the policy is mostly write-up, not new controls).

## Highest-leverage next 3 (sequence today if possible)

1. [ ] **Plaid production access** — meeting tomorrow morning. See Plaid setup block above.
2. [ ] **5 affiliate partner applications** — each is its own multi-day approval cycle. Stream B revenue ($300-1K/mo target) is dead until at least one approves.
3. [ ] **Fill remaining Patet Render env vars** — 15 minutes in browser. Server runs without them but Plaid + RevenueCat + Google OAuth all fail silently in prod.

---

## Patet — critical-path to first paying user

### Vendor signups (start in parallel — multi-day approvals)
- [ ] Plaid production access (dashboard.plaid.com — submit Plainly Digital LLC W-9, business description, expected transaction volume; 3-5 day approval)
- [ ] RevenueCat project (app.revenuecat.com; link iOS + Android apps once Apple/Play records exist)
- [ ] Google OAuth client (Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client ID for Web + iOS + Android)

### Affiliate partner signups (priority order — fastest approval first)
- [ ] Self Financial (credit builder, $20-50/signup, fastest per public docs)
- [ ] SoFi (student loan refi, $50-150/conversion)
- [ ] Marcus by Goldman / Ally HYSA ($25-100/account opening)
- [ ] YNAB referral (1mo free + $6/active user)
- [ ] Fidelity Roth IRA ($50-100/funded account)
- [ ] Submit Plainly Digital LLC W-9 to each approved partner
- [ ] Replace placeholder URLs in `Patet/server/src/db/affiliate.ts` (or wherever the catalog lives — locate during this step) with real partner tracking links

### Render config (browser, ~15 min)
Set these empty env vars on the Patet API service:
- [ ] `PLAID_CLIENT_ID` (production)
- [ ] `PLAID_SECRET` (production)
- [ ] `PLAID_ENV=production`
- [ ] `PLAID_WEBHOOK_SECRET`
- [ ] `GOOGLE_CLIENT_ID`
- [ ] `INTERNAL_API_KEY` — generate via `openssl rand -hex 32`
- [ ] `REVENUECAT_WEBHOOK_AUTH` (from RevenueCat dashboard → Project Settings → Webhooks)
- [ ] `PATET_LINKEDIN_ORG_ID` (after the Plainly Digital LinkedIn Company Page is provisioned — used by Patet Certified™ Add-to-Profile share)
- [x] Neon migrations 019 (coach_persona) + 020 (Patet Certified™ paid columns + vanity slug uniq idx) — ran 2026-05-11 via `npm run migrate` against `royal-lake-78408653` "plainly" project.

Then:
- [ ] **Import `render.yaml` via Render dashboard → Patet API → Blueprints.** Until this is done, the every-15-min onboarding-email cron does NOT fire. The email drip silently does nothing in production.
- [ ] Rotate Neon DB password (Neon dashboard → reset → paste new `DATABASE_URL` into Render env vars). Programmatic rotation needs a separate Neon API key.

### Post-deploy operational step (one command, after first prod deploy)
- [ ] `node dist/scripts/backfill-pii.js` — encrypts existing financial_snapshot + debt rows with the AES-256-GCM helpers shipped in migration 017. Idempotent; safe to rerun. Skipping this means existing rows stay plaintext until users overwrite them naturally.

### App Store Connect (browser + Figma)
- [ ] Create app record, bundle id `com.plainlydigital.patet`
- [ ] Generate Apple Connect API key (Users + Access → Keys)
- [ ] Fill `app/eas.json` `submit.production.ios.{appleId, ascAppId, appleTeamId}`
- [ ] Create 7 IAP products in App Store Connect:
  - `patet_pro_monthly` ($2.99/mo)
  - `patet_pro_annual` ($24.99/yr)
  - `patet_proplus_monthly` ($6.99/mo)
  - `patet_proplus_annual` ($57.99/yr)
  - `patet_boost` ($1.99 boost pack +50 calls)
  - `patet_power_boost` ($4.99 power pack +200 calls)
  - `patet_certified_credential` ($19 non-consumable — Patet Certified™ paid credential, monetization phase 2)
- [ ] Wire products → entitlements (`pro`, `pro_plus`) in RevenueCat dashboard
- [ ] Refine listing copy from `Patet/docs/APP-STORE-LISTING.md` drafts
- [ ] Design 6 iPhone 6.7" screenshots in Figma. Use `Patet/app/assets/screenshots/*.svg` as starter brand frames.
- [ ] Optional: 15-30 second video preview (lifts conversion ~25%)
- [ ] Upload assets + submit IAP for review (paired with binary)
- [ ] EAS production build: `cd Patet/app && eas build --platform ios --profile production`
- [ ] Run private TestFlight smoke test with 5-10 family/friends
- [ ] Submit for App Store review: `eas submit --platform ios --profile production`

### Google Play Console (browser + Figma)
- [ ] Create app, bundle id `com.plainlydigital.patet`
- [ ] Generate Play service account JSON; save to `Patet/app/google-play-key.json`; fill `eas.json` `serviceAccountKeyPath`
- [ ] Mirror 6 IAP products + listing copy
- [ ] Design 1024×500 feature graphic (use brand kit palette: black + green)
- [ ] EAS Android build: `cd Patet/app && eas build --platform android --profile production`
- [ ] Upload to internal testing track first → promote to production after smoke test passes

### Launch flip moment
- [ ] On Render, set `BETA_PRO_ACCESS=false`. No redeploy required.
- [ ] Verify free-tier rate limit enforces (hit any AI endpoint from a free-tier account; expect 429 after 10 calls/day)
- [ ] $50 Meta ads to "Gen Z + new grads + first-paycheck" lookalike audiences
- [ ] Monitor install→register→Plaid-connect→first-paid funnel; D1/D7 retention; CAC

### Trademark + legal (LLC business ops)
- [ ] File "Patet" Class 9 + 41 with USPTO (clearance complete 2026-05-09 — name is GO)
- [ ] Attorney review of `Patet/legal/06_Patet_Privacy_Policy.md` + `04_Patet_Terms_of_Service.md` before commercial launch

### Open product decisions (block code work until resolved)
- [ ] MFA-before-Plaid policy (audit deferred L10): mandatory? optional toggle in settings? recovery via email codes? recovery codes printed at enroll? — I can build it after the decision.
- [x] Spanish lesson content translation — done 2026-05-11 via Sonnet 4.6 machine translation. Native LATAM reviewer pass (BILINGUAL-3) still open before commercial Latam launch.

### Phase 2 / Phase 1 monetization — shipped 2026-05-11, follow-ups pending
- [x] Phase 1 (Glyphe persona packs + feature unlocks tied to lessons) shipped.
- [x] Phase 2 (\$19 Patet Certified™ credential, vanity slug, LinkedIn add-to-profile) shipped.
- [ ] Server-rendered PDF cert (deferred polish — SVG share-image already works for LinkedIn crawler)
- [ ] `/certified` marketing page on `plainly-psi.vercel.app` (Phase 2 plan called for it; not blocking purchase flow)
- [ ] Vanity slug picker UI inside the Patet profile (endpoint exists; UI is a follow-up)
- [ ] Glyphe system prompt cultural-context enhancement (BILINGUAL-6 — already has Spanish branch, polish-only)
- [ ] Supporting ES content surface wiring (BILINGUAL-7 — dailyContent/scenarios/finalAssessment/etc. consumers route through locale helpers; current ES files exist but lesson body is the only surface wired)
- [ ] Native LATAM Spanish reviewer pass (BILINGUAL-3 — $2K-$5K + 3 weeks before commercial Latam launch)

### Brand rename mop-up (Notch → Glyphe, 2026-05-11)
- [ ] **Glyphe USPTO + App Store + Play + .com clearance.** Notch was blocked by 10bit FX TM Reg #7691781; Glyphe has NOT been cleared. Do not file Glyphe TM or submit App Store listings under "Glyphe" until clearance passes.
- [ ] GitHub repo rename: `jbrock1981/Notch` → `jbrock1981/Glyphe` (gh CLI: `gh repo rename Glyphe` from `~/repos/42ly`)
- [ ] Vercel project rename: `notch` → `glyphe`, `notch-api` → `glyphe-api`
- [ ] Supabase project rename: `Notch` → `Glyphe` (or keep slug, just rename display)
- [ ] Local directory rename: `~/repos/42ly` → `~/repos/Glyphe` (also: `~/repos/Plainly` → `~/repos/Patet`, `~/repos/Vytally` → `~/repos/Vinla`, `~/repos/Accomplishly` → `~/repos/Winlet`, `~/repos/Pillarly` → `~/repos/Salvis`, `~/repos/Scamly` → `~/repos/Fraus`)

---

## Winlet — fastest path to first dollar

Per the multi-horizon revenue plan, Winlet should ship FIRST (95% built, 166 tests, deployed). Repeats the Patet store playbook but simpler scope (no Plaid).

- [ ] Wire RevenueCat (Free → Pro $2.99 → Pro+ $6.99) — same playbook as Patet
- [ ] Fill EAS credentials in `Winlet/eas.json`
- [ ] App Store Connect + Play Console app records for `com.plainlydigital.winlet`
- [ ] Listing copy + screenshots + IAP products
- [ ] EAS production builds → TestFlight + Play internal → submit
- [ ] Flip `BETA_PRO_ACCESS=false` on Winlet's Render service when live

---

## ClearDoc — rename + reposition (Phase 3b of revenue plan)

### Rename → BillPlain (or alternative)
- [ ] Clearance check (USPTO + App Store + Play + .com) on candidates: BillPlain, BillSpeak, Decode My Bill
- [ ] Pick winner

### Reposition to medical-bills primary lane
- [ ] Update marketing copy: medical bills primary, "any document" as secondary mode
- [ ] Add 3 features to lift retention: bill history, family share deep link, CPT/HCPCS code lookup
- [ ] Pricing change: drop monthly to $4.99/mo OR add $29.99/yr (current $7.99/mo monthly-only causes 60-80% utility-app churn)
- [ ] Resubmit under new name + new metadata

---

## SitterSheet — hold pattern

Per revenue plan, SitterSheet has a $50-300 MRR ceiling and competes with NYC web competitor's iOS roadmap. Not worth Phase 1-3 cycles.
- [ ] No action this quarter.

---

## Vinla — pre-launch reset (6-8 weeks of work)

- [ ] Reposition from "family health" → "personal wellness with AI coach" (closer to actual code)
- [ ] Fix RLS gaps in Supabase (production-blocker security)
- [ ] Fix client-side tier gating (currently bypassable)
- [ ] After above lands: same store-submission playbook as Patet
- [ ] Currently scoped lower priority than Patet/Winlet per plan

---

## Glyphe (AI life advisor) — clearance required before public launch

The standalone life-advisor app was renamed Notch → **Glyphe** on 2026-05-11
after the 10bit FX TM block surfaced. Same name is now the AI-coach
personality across Patet, Vinla, Winlet, and the life-advisor app itself.

- [ ] **Glyphe USPTO clearance** — search Class 9 / 41 / 42. Glyphe has NOT
  been formally cleared yet. Do not file the TM application or submit App
  Store listings under "Glyphe" until USPTO + App Store + Play + .com all
  return clear.
- [ ] After clearance: file Class 9 + 42 for the life-advisor app +
  cross-portfolio coach name. See `project_app_name_clearance.md` for the
  full filing recommendation.
- [ ] After clearance: store submission (App Store + Play Console under
  Glyphe name + bundle id) for the standalone life-advisor app.

---

## Tradingly — internal only

- [ ] Phase 4E (live trading) pending legal review. Hold until reviewer signs off.
- [ ] Daily morning server failure was diagnosed (task #10). Confirm fix is sticky.

---

## CastFreely — Lauri's app

Owned by Lauri. No actions on your side beyond support.

---

## Fraus + Salvis — parked until 2027

- [ ] Run $50 Meta ads validation when ready to revisit (per `project_fraus_salvis_todo.md`). Phase 1 landing pages already scaffolded.

---

## PlainlyDigital marketing site

- [ ] After Patet first paying user lands: resubmit `https://plainlydigital.com/sitemap-index.xml` in Google Search Console (replaces old static `/sitemap.xml`)
- [ ] As each app submits to stores: update `src/data/apps.ts` `status` field for that app from `coming-soon` / `in-beta` → `available`
- [ ] Decide if Vinla, Winlet, Glyphe (renamed) need full product pages on the marketing site beyond their current Coming Soon stubs — model on `src/pages/patet/index.astro` if so

---

## LLC business operations

- [ ] Trademark filings (USPTO Class 9 + 41):
  - [ ] Patet (clearance done — file)
  - [ ] Vinla (clearance done per memory — file)
  - [ ] Winlet (clearance done per memory — file)
- [ ] W-9 registration with every affiliate program as they approve
- [ ] Attorney review for ToS + Privacy on every app at first commercial launch
- [ ] Confirm GCP billing account `019368-94B72C-5B073A` (apps@plainlydigital.com) is current and $350K AI startup credits balance is intact

---

## GCP migration (per `project_gcp_migration.md`)

Glyphe already migrated. Cloud Build pattern lives in `PlainlyDigital/cloudbuild.yaml`.

- [ ] Patet — defer until first paying user (~1-2 weeks effort). When ready: provision GCP project under apps-org, mirror Cloud Build trigger, switch DNS.
- [ ] Vinla — same pattern, after Patet
- [ ] Winlet — same pattern, after Patet
- [ ] CastFreely — out of scope (Lauri's)

---

## Local dev environment

- [ ] Rename local directories to match GitHub repos:
  - `~/repos/Plainly/` → `~/repos/Patet/`
  - `~/repos/Vytally/` → `~/repos/Vinla/` (if not already done)
  - `~/repos/Accomplishly/` → `~/repos/Winlet/` (if not already done)
  - `~/repos/Pillarly/` → `~/repos/Salvis/` (if not already done)
  - `~/repos/Scamly/` → `~/repos/Fraus/` (if not already done)
  - `~/repos/42ly/` → `~/repos/Glyphe/` (or new name once chosen)
- [ ] After renames, update memory cross-refs (project_repos.md, etc.) to new paths

---

## Audit holdouts (you decide whether to spend code time on these now)

| Item | Effort | Pre-launch? |
|---|---|---|
| MFA before Plaid connect (audit L10) | 2-3 days code | Product decision needed first |
| Spanish lesson content translation | 3 weeks + $2.5-5.5K | Latam launch only |
| `react-native-markdown-display` 6.x downgrade | 1 day + device QA | Defensive only |

Everything else from the audit is closed.

---

## Recently completed (for context — do not re-do)

- ✅ Anthropic, JWT, encryption, internal-API keys rotated on Render (2026-05-09)
- ✅ Persisted account lockout (audit defer) — migration 015
- ✅ Persistent JWT token revocation — migration 016
- ✅ Per-IQ-result dynamic OG image endpoint
- ✅ CCPA/GDPR data export endpoint + mobile screen (audit M14)
- ✅ Financial PII column encryption — migration 017 Phase A (audit M6)
- ✅ JWT httpOnly cookie on web (audit H1)
- ✅ Onboarding email drip (welcome + 24h + 3d + 7d)
- ✅ Referral program (50 bonus calls each)
- ✅ App Store screenshot SVG draft templates (6 frames)
- ✅ App icon + splash + adaptive icon (1024×1024 + 1284×2778)
- ✅ Marketing site `/patet/` page + `/iq/` funnel landing
- ✅ Open Graph image + sitemap + JSON-LD structured data
- ✅ Patet privacy.mdx + terms.mdx on marketing site (App Store submission unblocker)
- ✅ USPTO + iOS/Play Store name clearance complete for Patet, Vinla, Winlet
- ✅ GitHub Actions workflow removed (portfolio uses Cloud Build)
- ✅ Apple Developer ($99/yr) + Google Play ($25 once) accounts funded
- ✅ All major renames: Plainly→Patet, Vytally→Vinla, Accomplishly→Winlet, Pillarly→Salvis, Scamly→Fraus, 42ly→Glyphe (Glyphe needs rename due to TM block)
