# Plainly Digital — Roadmap

Anything not shipping in v1.0 of the marketing site lives here.

> **v1.0 ships:** Astro 5 + MDX static site at `plainlydigital.com`. Hero + 6 app pages (ClearDoc + SitterSheet deep, 4 coming-soon). Parent + per-app privacy/ToS. Tennessee law. Single contact `apps@plainlydigital.com`. Hand-rolled SVG logos + 1024px PNG export. Cloudflare Pages hosting with full security headers, RFC 9116 security.txt, no third-party JS. Build-only CI + Dependabot + weekly npm-audit notification.

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
- ✅ **Domain `plainlydigital.com`** — registered. DNS migrated to Cloudflare nameservers.
- ✅ **`apps@plainlydigital.com`** — single contact across all apps + legal docs. Hosted on **Microsoft 365** (Zoho was paid-only at the entry tier; M365 was the most reliable option).
- ⏳ **DKIM / SPF / DMARC** — need to confirm M365's records are in Cloudflare DNS and that mail from `apps@plainlydigital.com` passes all three at gmail/outlook recipients before any launch announcements.

### Marketing site (plainlydigital.com)
- ✅ **Built + deployed 2026-05-04** to **Cloudflare Pages** from repo `jbrock1981/PlainlyDigital`. Astro 5 + MDX, no third-party JS, full security headers (HSTS, CSP, X-Frame-Options:DENY, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP/CORP), RFC 9116 `/.well-known/security.txt`.
- ✅ **14 pages** built clean: home, 6 app pages (ClearDoc + SitterSheet deep, 4 coming-soon), per-app + parent privacy/ToS in MDX, /about. Tennessee governing law throughout.
- ✅ **7 SVG logos** + 1024×1024 PNG export script for app store icons.
- ✅ **CI**: minimal — build-only on PR + weekly `npm audit --audit-level=moderate` notification. Dependabot daily security PRs.
- ⏳ **Real device screenshots** replace SVG mobile mockups after first EAS internal builds.
- ⏳ **App Store + Play Store badge links** turn ON once apps are live.

### Google Cloud / Firebase
- ✅ **Google Cloud for Startups** — approved 2026-05-04. Credits awarded under `apps@plainlydigital.com`.
- ✅ **Billing account** `019368-94B72C-5B073A` ("Plainly Digital LLC"). All Plainly Digital LLC GCP projects bill against this and consume the startup credits.
- ✅ **Cloud Identity org `apps-org`** (auto-created by Google) — `611419173109`. apps@plainlydigital.com is `roles/resourcemanager.organizationAdmin` + `roles/billing.admin` + `roles/iam.workforcePoolAdmin` + `roles/resourcemanager.projectMover`.
- ✅ **GCP project `cleardoc-plainlydigital`** (`872804656503`) — under `apps-org`, billing linked. Firebase added. Firestore Native (us-central1), rules + indexes deployed, 3 Cloud Functions deployed, secrets in Secret Manager.
- ✅ **GCP project `sittersheet-plainlydigital`** (`116927353996`) — same shape, 5 Cloud Functions deployed.
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

### Self-hosted CI/CD on GCP (FUTURE)
- Build a private CI/CD pipeline on Cloud Build / Cloud Run that all Plainly Digital repos use instead of GitHub Actions minutes. Reduces external dependency, lets us run ZAP + heavyweight scans without Actions runner limits, keeps build secrets inside the GCP perimeter.
- Out of scope until apps are live + revenue-generating.

### Trademark + DBA
- ⏳ **"Plainly Digital"** trademark search (USPTO TESS). If clean, file ITU (~$350).
- ⏳ **"ClearDoc"** + **"SitterSheet"** searches. Both are crowded namespaces — likely descriptive-mark strategy or alternative naming.
- ⏳ **TN DBA registration** if Plainly Digital LLC's articles don't already cover these app names.
