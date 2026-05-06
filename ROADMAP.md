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
- ✅ **Built + deployed 2026-05-04** to **Cloudflare Pages** from repo `jbrock1981/PlainlyDigital` — staging/scaffolding deploy only; site never resolved at `plainlydigital.com` (DNS still on GoDaddy parking). Astro 5 + MDX, no third-party JS, full security headers (HSTS, CSP, X-Frame-Options:DENY, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP/CORP), RFC 9116 `/.well-known/security.txt`.
- ✅ **Migrated to Firebase Hosting 2026-05-05** under GCP project `plainlydigital-www` (apps-org). Site live at `https://plainlydigital.web.app/` (default site `plainlydigital`, derived from project ID with `-www` stripped). All 14 pages return 200, all 8 security headers present, Astro hashed assets cached 1y immutable, `/icons/*` cached 24h. First Cloud Build deploy SUCCEEDED in 48s.
- 🔄 **Custom domain `plainlydigital.com`** — Firebase Console step pending (add custom domain → capture A/AAAA/TXT records → add to Cloud DNS → GoDaddy nameserver swap). Cloudflare Pages decommissioned post-cutover.
- 🔄 **Cloud Build trigger on push to main** — pipeline verified working via manual `gcloud builds submit`. Auto-deploy trigger pending Google Cloud Build GitHub App authorization for `jbrock1981` (browser step at https://github.com/marketplace/google-cloud-build).
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

### App migration: Vercel/Render → GCP (PLANNED)

**Why:** every Plainly Digital LLC app should bill against the same GCP startup credits. Today the older apps run on Vercel + Render + Neon, which billed against personal cards before the LLC + credits existed. Migration consolidates: one bill, one identity perimeter, credits cover spend, and the self-hosted CI/CD plan above can target a single deployment surface.

**Scope:** all Plainly Digital LLC apps. **CastFreely is explicitly excluded** — it's a separate LLC owned by Lauri Brock, stays on its current Vercel/Neon stack.

**Apps to migrate, current state:**

| App | Stack today | GCP target | Notes |
|---|---|---|---|
| **Plainly** (finlit) | Vercel (web) + Render (Node API) + Neon Postgres | Cloud Run for the Node API + Firebase Hosting (or Cloud CDN) for the Expo web build; **Neon stays** (managed Postgres at Neon is cheaper than Cloud SQL at our scale and works fine over the public internet from Cloud Run). | Plaid keys + Anthropic key follow into Secret Manager. Sentry stays where it is. |
| **Vytally** (health) | Vercel (Next-style + serverless) + Supabase Postgres + Supabase Auth | Cloud Run for the API + Firebase Hosting for the static export; **Supabase stays** for now (Auth + RLS migration is its own large project). | RLS hardening is a pre-launch blocker that must NOT be derailed by the migration. |
| **Accomplishly** | Vercel + Neon | Cloud Run + Firebase Hosting; Neon stays. | Currently DEPLOYED & LIVE — migration must be zero-downtime via DNS cutover. |
| **AI Life Advisor** (formerly 42ly) | Vercel (frontend at 42ly.vercel.app + API at 42ly-api.vercel.app) + Supabase | Cloud Run for the API + Firebase Hosting for the frontend. Supabase stays. | Despite the marketing site saying "coming soon," the underlying 42ly build is feature-complete and deployed in invite-only beta. Migration applies. |
| **Tradingly** | Vercel (Next.js) + Render (FastAPI 512MB) + Neon Postgres + SQLite cache | Cloud Run for FastAPI (fixes Render 30s timeout pain point + the keep-alive sleep-on-Starter issue) + Firebase Hosting for the Next.js. Neon stays. SQLite cache is per-instance and can stay local in the container. | Phase 4B.3 already moved durable state to Postgres specifically because Render Starter ephemeral SQLite was breaking autopilot. The migration unblocks Phase 4E (live trading) since "backend reliability upgrade" is in the Phase 4E gate. |
| **Scamly + Pillarly** | Phase 1 landing pages (validate-then-build via $50 Meta ads) | Born on GCP if/when they progress to MVP. | No migration step — gate on validation outcome first. |

**Exclusions:**
- **CastFreely** — separate LLC (Lauri Brock, CastFreely LLC pending). Stays on Vercel/Neon. CastFreely will get its own Google Cloud Startups application under Lauri's name when CastFreely LLC is formed; do NOT pull it onto the Plainly Digital billing.
- **Advisedly** — separate LLC entirely. Already on its own infra path.

**Migration order (riskiest last so we learn first on the lowest-stakes apps):**
1. **AI Life Advisor** (42ly) — invite-only beta, lowest blast radius.
2. **Plainly** (finlit) — pre-beta, no live users yet.
3. **Tradingly** — small allow-listed user base (family + Papous), unblocks Phase 4E.
4. **Vytally** — family beta, larger blast radius.
5. **Accomplishly** — DEPLOYED & LIVE, zero-downtime cutover required, do this last after the pattern is proven.

**Standard migration recipe (per app):**
- Create `<app>-plainlydigital` GCP project under `apps-org`, link billing.
- Containerize the API (Dockerfile if not already). Push to Artifact Registry, deploy to Cloud Run.
- Frontend: replace Vercel build pipeline with Firebase Hosting deploy (or Cloud CDN if more dynamic).
- Move secrets from Vercel/Render env vars → Secret Manager. Re-deploy with `--set-secrets`.
- Verify the Postgres host (Neon/Supabase) is reachable from Cloud Run egress IP — usually fine, but Neon's IP allowlist may need updating.
- Cutover DNS at the per-domain authoritative provider (verify with `dig <domain> NS +short` per domain — earlier "all PD domains on Cloudflare" claim was incorrect; `plainlydigital.com` itself is moving to Cloud DNS, not Cloudflare) — Cloud Run domain mapping or Firebase Hosting custom domain. Keep Vercel/Render running until DNS propagates, then decommission.
- Final step per migration: cancel Vercel + Render paid plans for that app, document in this tracker.

**Out of scope for this migration (deferred):**
- Moving Neon → Cloud SQL. Neon's serverless Postgres is cheaper at our scale and the dev experience is better. Re-evaluate after $1K MRR per app or when Neon throws scale issues.
- Moving Supabase Auth → Firebase Auth or Identity Platform. Big refactor, not blocked by hosting migration.

### Self-hosted CI/CD on GCP (FUTURE)
- Build a private CI/CD pipeline on Cloud Build / Cloud Run that all Plainly Digital repos use instead of GitHub Actions minutes. Reduces external dependency, lets us run ZAP + heavyweight scans without Actions runner limits, keeps build secrets inside the GCP perimeter.
- Naturally builds on the migration above — once all PD apps deploy to GCP, the CI/CD pipeline lives next to them.
- Out of scope until apps are live + revenue-generating.

### Trademark + DBA
- ⏳ **"Plainly Digital"** trademark search (USPTO TESS). If clean, file ITU (~$350).
- ⏳ **"ClearDoc"** + **"SitterSheet"** searches. Both are crowded namespaces — likely descriptive-mark strategy or alternative naming.
- ⏳ **TN DBA registration** if Plainly Digital LLC's articles don't already cover these app names.
