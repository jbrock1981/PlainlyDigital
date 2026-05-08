# Plainly Digital — Roadmap

Anything not shipping in v1.0 of the marketing site lives here.

> **v1.0 ships:** Astro 5 + MDX static site at `plainlydigital.com`. Hero + 6 app pages (ClearDoc + SitterSheet deep, 4 coming-soon). Parent + per-app privacy/ToS. Tennessee law. Single contact `apps@plainlydigital.com`. Hand-rolled SVG logos + 1024px PNG export. Firebase Hosting (GCP project `plainlydigital-www` under `apps-org`) with full security headers, RFC 9116 security.txt, no third-party JS. Cloud Build CI/CD on push to main. Dependabot + weekly npm-audit notification.

---

## v1.x — within 60 days of launch

### Content
- **Real device screenshots** — replace SVG mobile mockups on `/cleardoc` and `/sittersheet` once the first EAS internal builds are taken. Mobile-only — no desktop or tablet variants.
- **Per-app press kit page** — `/cleardoc/press`, `/sittersheet/press` — logo PNG, brand colors, descriptions journalists can copy/paste.
- **App Store + Play Store badge links** turn ON once the apps are live. Until then, all CTAs say "Coming soon to App Store + Google Play" with no link.
- **Founder bio expansion** on `/about` — keep the cybersecurity-engineer framing, add a one-paragraph "why these apps" story. Stays anonymous-by-default unless we decide otherwise.

### Marketing infrastructure
- **Cloudflare Web Analytics** — cookieless, free, minimal. Turn on once we have anything worth measuring.
- **Email signup form** — "notify me when X launches." Cloudflare Workers + Resend for delivery. Defer until traffic justifies the spam-prevention work (honeypot, Cloudflare Turnstile).
- **Blog / changelog section** at `/blog` — short release notes per app + occasional "how I built this" posts. Astro content collections.

### Internationalization
- English-only at v1. Add Spanish + French once we have data on where the apps are downloaded most. Astro i18n routing handles this cleanly.

### Tech debt
- The Astro sitemap integration crashed during scaffolding, so we hand-rolled `public/sitemap.xml`. Revisit `@astrojs/sitemap` after it ships a fix — re-enabling will keep the sitemap in sync with the routes automatically.
- `linkinator` skip-list currently excludes `plainlydigital.com` to avoid false negatives during development. Once the site is live, drop the skip and let it verify the live links too.
- The pa11y-ci dependency was dropped due to a vulnerable puppeteer chain. Revisit when pa11y ships a Playwright-based variant.

---

## v2 — after the suite is live (5+ apps shipped)

- **Suite navigation** — sticky cross-app links so visitors on `/sittersheet` can jump to `/cleardoc` without going through home.
- **Unified search** — Algolia DocSearch or Pagefind across all app pages + blog.
- **Multi-author blog** — once Plainly Digital has more than one person writing.
- **Customer testimonial pages** per app — only after the apps actually have customers.
- **Open positions page** at `/jobs` — only if we hire.

---

## Recurring security + hygiene

- Weekly `npm audit --audit-level=moderate` via GitHub Actions → opens issue on findings (`security-audit.yml`).
- Daily Dependabot — security PRs auto-opened, group dev/non-dev separately.
- Quarterly OWASP ZAP baseline scan against the deployed site. Manual from local Docker, results in `docs/security-scans/`.
- Re-validate `_headers` against Mozilla Observatory + securityheaders.com after every deploy that touches it.
- Re-validate `.well-known/security.txt` `Expires:` field annually (currently 2027-05-01).
- Annual external pentest budget item — not a v1 task.

---

## Plainly Digital LLC — master tracker (operations)

NOT marketing-site work — lives here because no other repo is the right home. This is the running source of truth for the parent-company state.

### Identity + email
- ✅ **Domain `plainlydigital.com`** — registered at GoDaddy.
- 🔄 **DNS authority** — Cloud DNS managed zone `plainlydigital-com` created 2026-05-05 in project `plainlydigital-www` with NS values `ns-cloud-a{1,2,3,4}.googledomains.com.`. **Pending GoDaddy nameserver swap** (browser step). Until then, GoDaddy nameservers remain authoritative and `plainlydigital.com` still resolves to GoDaddy parking. Plan: `we-need-to-move-silly-rose.md`.
- ✅ **`apps@plainlydigital.com`** — single contact across all apps + legal docs. Hosted on **Microsoft 365** (Zoho was paid-only at the entry tier; M365 was the most reliable option).
- ⏳ **DKIM / SPF / DMARC** — audit GoDaddy DNS export BEFORE the nameserver swap to capture any M365 records currently in place. Recreate in Cloud DNS pre-swap or mail breaks. After cutover, verify mail from `apps@plainlydigital.com` passes all three at gmail/outlook recipients.

### Marketing site (plainlydigital.com)
- ✅ **Built 2026-05-04** from repo `jbrock1981/PlainlyDigital` — Astro 5 + MDX, no third-party JS, full security headers (HSTS, CSP, X-Frame-Options:DENY, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP/CORP), RFC 9116 `/.well-known/security.txt`. (Note: an earlier ROADMAP entry claimed a Cloudflare Pages deploy on this date; verified 2026-05-06 that no Cloudflare project ever existed — that ✅ was optimistically marked. Site only ever deployed to Firebase Hosting.)
- ✅ **Migrated to Firebase Hosting 2026-05-05** under GCP project `plainlydigital-www` (apps-org). Site live at `https://plainlydigital.web.app/` (default site `plainlydigital`, derived from project ID with `-www` stripped). All 14 pages return 200, all 8 security headers present, Astro hashed assets cached 1y immutable, `/icons/*` cached 24h. First Cloud Build deploy SUCCEEDED in 48s.
- ✅ **Custom domain `plainlydigital.com` + `www.plainlydigital.com`** — cutover 2026-05-06. NS swapped from GoDaddy to Cloud DNS, all email-preserving records (MX/SPF/DMARC/autodiscover/M365 tenant TXT) migrated, Firebase custom domain verified, Google Trust Services cert provisioned (expires 2026-08-04, auto-renews). www 301-redirects to apex. Cloudflare Pages decommissioned same day.
- ✅ **Cloud Build trigger on push to main** — `deploy-on-push-main` wired 2026-05-06. GitHub App authorized for `jbrock1981/PlainlyDigital`, trigger uses Compute Engine default SA, end-to-end test passed (42s build, immediate deploy). Every push to `main` now auto-deploys.
- ✅ **14 pages** built clean: home, 6 app pages (ClearDoc + SitterSheet deep, 4 coming-soon), per-app + parent privacy/ToS in MDX, /about. Tennessee governing law throughout.
- ✅ **7 SVG logos** + 1024×1024 PNG export script for app store icons. PNG generation now part of Cloud Build pipeline (icons:build → build → lint:links → deploy).
- ✅ **CI**: minimal — build-only on PR + weekly `npm audit --audit-level=moderate` notification. Dependabot daily security PRs. Production deploys via Cloud Build (manual until trigger is wired).
- ✅ **Claude Code guardrails** — repo-level CLAUDE.md, .claude/settings.json (allow/deny), .claude/hooks.json (truncation guard, prettier auto-format, pre-commit build gate), .claude/skills/ (deploy.md, dns.md, memory-sync.md). Modeled on Advisedly. To be extracted as a `plainlydigital-claude-config` template once validated.
- ⏳ **Real device screenshots** replace SVG mobile mockups after first EAS internal builds.
- ⏳ **App Store + Play Store badge links** turn ON once apps are live.

### Google Cloud / Firebase
- ✅ **Google Cloud for Startups** — approved 2026-05-04. Credits awarded under `apps@plainlydigital.com`.
- ✅ **Billing account** `019368-94B72C-5B073A` ("Plainly Digital LLC"). All Plainly Digital LLC GCP projects bill against this and consume the startup credits.
- ✅ **Cloud Identity org `apps-org`** (auto-created by Google) — `611419173109`. apps@plainlydigital.com is `roles/resourcemanager.organizationAdmin` + `roles/billing.admin` + `roles/iam.workforcePoolAdmin` + `roles/resourcemanager.projectMover`.
- ✅ **GCP project `cleardoc-plainlydigital`** (`872804656503`) — under `apps-org`, billing linked. Firebase added. Firestore Native (us-central1), rules + indexes deployed, 3 Cloud Functions deployed, secrets in Secret Manager.
- ✅ **GCP project `sittersheet-plainlydigital`** (`116927353996`) — same shape, 5 Cloud Functions deployed.
- ✅ **GCP project `plainlydigital-www`** (`331893043173`) — created 2026-05-05 under `apps-org`, billing linked. Firebase Hosting (default site `plainlydigital`), Cloud DNS zone `plainlydigital-com`, Cloud Build pipeline. **`addFirebase` CLI worked clean for this project** — the previous 403 gotcha appears scoped to projects moved between orgs, not new ones created under apps-org from the start. Compute SA (not Cloud Build SA) is what runs builds on new GCP projects post-2024 — granted `firebase.admin`, `firebasehosting.admin`, `cloudbuild.builds.builder`, `storage.objectViewer`, `logging.logWriter`.
- ⚠️ **`project-b9104919-708e-4dd1-be2`** ("My First Project") — auto-created sandbox, not used. Delete or repurpose later.
- ⏳ **GCP billing budgets** — set in Console → Billing → Budgets: `$50/mo` ClearDoc + `$30/mo` SitterSheet, alerts at 50%/90%/100% to apps@plainlydigital.com.
- ⏳ **Firestore TTL on `ai_audit/{date}/calls/{requestId}`** — collection group `calls`, field `expiresAt`. Auto-delete 30d. Set per-project.
- ⏳ **Anthropic keys** — currently both apps use a single shared key. Generate two project-scoped keys at console.anthropic.com and re-run `firebase functions:secrets:set ANTHROPIC_API_KEY` from each app's `functions/` directory.

### Apple Developer
- ✅ **Account paid, pending approval** — enrolled under JBrock dependent (couldn't enroll directly: old Apple ID on phone number was disabled and unrecoverable, Google Voice number triggered captcha block). Once approved, transfer / link to Plainly Digital LLC.
- ⏳ **Small Business Program enrollment** — 15% cut under $1M. Apply once main account is approved.
- ⏳ **D-U-N-S verification** at the org-account level once the account transitions out of dependent ownership.

### Google Play Console
- ⏳ **Account creation** — $25 one-time at play.google.com/console. Enroll as **Organization** with Plainly Digital LLC D-U-N-S. Use `apps@plainlydigital.com`. Same account is used for ClearDoc + SitterSheet (and future apps).

### RevenueCat
- ⏳ **Account creation** at revenuecat.com. Free until $2.5K MRR. Two separate projects under one account: "ClearDoc" + "SitterSheet".
- ⏳ **Webhooks** point at the deployed Cloud Function URLs (in each app's `LAUNCH.md`). Bearer token rotated into Secret Manager `REVENUECAT_WEBHOOK_SECRET` after webhook is created.
- ⏳ **Products configured** per `LAUNCH.md` of each app (ClearDoc: monthly + pack20; SitterSheet: unlock-only).

### Anthropic
- ✅ **Existing API key** — works, currently shared between apps.
- ⏳ **Per-app key rotation** — generate `cleardoc-prod` and `sittersheet-prod` keys, scope each, blast-radius isolation.

### App migration: Vercel/Render → GCP (IN FLIGHT)

**Why:** every Plainly Digital LLC app should bill against the same GCP startup credits. Today the older apps run on Vercel + Render + Neon + Supabase, which billed against personal cards before the LLC + credits existed. Migration consolidates: one bill, one identity perimeter, credits cover spend.

**Scope expansion 2026-05-05:** original recipe was "compute migrates, DBs/Auth stay." With the **AI Startups credit pool at $350K** (granted because every PD app uses Claude AI — see `reference_plainly_gcp_billing.md`), the cost-saving rationale for keeping Neon/Supabase no longer applies. **For the Fiscus + Vitaliter sub-passes, scope is full GCP consolidation:** Cloud SQL replaces Neon (Fiscus) and Supabase Postgres (Vitaliter); Firebase Auth replaces Supabase Auth (Vitaliter); a hybrid GitHub Actions + Cloud Build CI/CD pipeline (originally "FUTURE", below) is pulled forward and built as a reusable template `plainlydigital-ci-templates`. Other apps (AI Life Advisor, Tradingly, Winlet) keep the original "compute-only" recipe until they hit a similar inflection point.

Per-domain DNS authority is verified per migration via `dig <domain> NS +short` — the earlier "all PD domains already on Cloudflare DNS" claim was wrong. `plainlydigital.com` itself was on GoDaddy parking until 2026-05-05 and is migrating to **Cloud DNS** (managed zone `plainlydigital-com` in `plainlydigital-www`).

**Apps to migrate, current state:**

| App | Stack today | GCP target | Notes |
|---|---|---|---|
| **Fiscus** (formerly Plainly) | Vercel (web) + Render (Node API) + Neon Postgres | Cloud Run + Firebase Hosting + **Cloud SQL Postgres** (replacing Neon). Domain `fiscus.app`. | Trademark search clean 2026-05-05 — rename + GCP migration bundled per plan `we-have-cleardoc-and-radiant-cookie.md`. Cross-platform web + mobile retained (Rocket Money pattern). Already on self-issued JWTs, no Auth swap needed. |
| **Vitaliter** (formerly Vinla) | Vercel (Next-style + serverless) + Supabase Postgres + Supabase Auth | Cloud Run + Firebase Hosting + **Cloud SQL Postgres** + **Firebase Auth** + **mobile-only** (web stripped). No new domain — marketing landing is a section on `plainlydigital.com`. | Trademark search clean 2026-05-05. Web strip + Supabase Auth → Firebase Auth + Cloud SQL bundled in same plan. The **CRITICAL pre-launch RLS blocker is superseded** by the Auth swap: server-side authorization on Cloud SQL queries tied to Firebase UIDs replaces RLS. |
| **Winlet** (formerly Accomplishly) | Vercel + Neon | Cloud Run + Firebase Hosting; Neon stays (compute-only recipe). | Currently DEPLOYED & LIVE — migration must be zero-downtime via DNS cutover. Re-evaluate Cloud SQL once Fiscus pattern is proven. |
| **AI Life Advisor** (Notch, formerly 42ly) | Vercel (frontend at notch.vercel.app + API at notch-api.vercel.app) + Supabase | Cloud Run + Firebase Hosting. Supabase stays (compute-only recipe). | Despite the marketing site saying "coming soon," the underlying Notch build is feature-complete and deployed in invite-only beta. Migration applies. |
| **Tradingly** | Vercel (Next.js) + Render (FastAPI 512MB) + Neon Postgres + SQLite cache | Cloud Run for FastAPI + Firebase Hosting for Next.js. Neon stays (compute-only recipe). | Cloud Run fixes Render 30s timeout + keep-alive idle sleep that breaks autopilot tick. Phase 4B.3 already moved durable state to Postgres specifically because of this. **Migration is REQUIRED before Phase 4E** (live trading) — backend reliability upgrade is in the Phase 4E legal gate. |
| **Fraus + Pillarly** | Phase 1 landing pages (validate-then-build via $50 Meta ads) | Born on GCP if/when they progress to MVP. | No migration step — gate on validation outcome first. |

**Exclusions:**
- **CastFreely** — separate LLC (Lauri Brock, CastFreely LLC pending). Stays on Vercel/Neon. CastFreely will get its own Google Cloud Startups application under Lauri's name when CastFreely LLC is formed; do NOT pull it onto the Plainly Digital billing.
- **Advisedly** — separate LLC entirely. Already on its own infra path.

**Migration order (riskiest last so we learn first on the lowest-stakes apps):**
1. **AI Life Advisor** (Notch) — invite-only beta, lowest blast radius. Compute-only recipe.
2. **Fiscus** (formerly Plainly) — pre-beta, no live users yet. **Full GCP consolidation** (Cloud SQL).
3. **Tradingly** — small allow-listed user base (family + Papous), unblocks Phase 4E. Compute-only recipe.
4. **Vitaliter** (formerly Vinla) — family beta. **Full GCP consolidation** (Cloud SQL + Firebase Auth + mobile-only).
5. **Winlet** (formerly Accomplishly) — DEPLOYED & LIVE, zero-downtime cutover required, do this last after the pattern is proven. Compute-only recipe.

**Plans:**
- Marketing site migration: `C:\Users\jbroc\.claude\plans\we-need-to-move-silly-rose.md`
- Fiscus + Vitaliter combined plan: `C:\Users\jbroc\.claude\plans\we-have-cleardoc-and-radiant-cookie.md`
- AI Life Advisor / Tradingly / Winlet plans: not yet drafted.

**Standard recipes:**

*Compute-only (AI Life Advisor, Tradingly, Winlet):*
- New `<app>-plainlydigital` GCP project under `apps-org`, link billing.
- Containerize the API. Push to Artifact Registry, deploy to Cloud Run.
- Frontend: Firebase Hosting deploy (or Cloud CDN if more dynamic).
- Secrets: Vercel/Render env vars → Secret Manager.
- Verify Postgres host (Neon/Supabase) reachable from Cloud Run egress IP. Update IP allowlists if needed.
- DNS cutover at the per-domain authoritative provider. Verify NS first.
- Cancel Vercel + Render paid plans post-DNS propagation.

*Full consolidation (Fiscus, Vitaliter):* compute-only steps PLUS:
- Cloud SQL Postgres provisioning, schema migration via `pg_dump`/`pg_restore` (Fiscus from Neon, Vitaliter from Supabase).
- Firebase Auth provisioning (Vitaliter only — Fiscus already on self-issued JWTs).
- Hybrid CI/CD pipeline using the `plainlydigital-ci-templates` repo: GitHub Actions for tests + lint, Cloud Build for deploy.
- Vitaliter only: strip the web layer (`apps/web/` → deleted), update repo to `mobile/` + `api/` + `migrations/` only.

**Status (2026-05-06):**
- ✅ **Marketing site sub-pass (`plainlydigital-www`)** — site live at `https://plainlydigital.com/` (cutover 2026-05-06), Cloud Build auto-deploy on push to main (`deploy-on-push-main` trigger wired 2026-05-06).
- ⏳ **Fiscus** — plan exists, no execution started. Renamed local + GitHub repo not yet performed.
- ⏳ **Vitaliter** — same status. `C:\Users\jbroc\Vinla` is empty locally; clone before any work.
- ⏳ **AI Life Advisor / Tradingly / Winlet** — plans not drafted; original ordering still applies.

### Self-hosted CI/CD on GCP (PARTIALLY IN FLIGHT)
- ✅ **Marketing site (`plainlydigital-www`)** — Cloud Build auto-deploy on push to main wired 2026-05-06 (`deploy-on-push-main`, ~42s end-to-end).
- ⏳ **`plainlydigital-ci-templates` repo** — pulled forward from "FUTURE" as part of the Fiscus + Vitaliter sub-pass. Hybrid GitHub Actions (tests + lint) + Cloud Build (deploy). Reusable across all PD repos. Build during Fiscus migration so Vitaliter can adopt cleanly. Other apps (ClearDoc, SitterSheet, AI Life Advisor, Winlet, Tradingly) adopt later as they get re-deployed.
- ⏳ **`plainlydigital-claude-config` template** — extract the PlainlyDigital repo's `CLAUDE.md` + `.claude/settings.json` + `.claude/hooks.json` + `.claude/skills/` (truncation guard, prettier auto-format, pre-commit build gate, deploy/dns/memory-sync skills) once validated. Adopters: ClearDoc, SitterSheet, Fiscus, Vitaliter, AI Life Advisor, Winlet, Tradingly.
- ⏳ **Heavy-scan workloads** (OWASP ZAP, dep-graph SAST, etc.) move into Cloud Build once template is stable. Removes GitHub Actions runner-minute pressure and keeps build secrets inside the GCP perimeter.

### Trademark + DBA
- ⏳ **"Plainly Digital"** trademark search (USPTO TESS). If clean, file ITU (~$350).
- ⏳ **"ClearDoc"** + **"SitterSheet"** searches. Both are crowded namespaces — likely descriptive-mark strategy or alternative naming.
- ⏳ **TN DBA registration** if Plainly Digital LLC's articles don't already cover these app names.
