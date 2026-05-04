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

## Plainly Digital LLC — operations

These are NOT marketing-site tasks but live here because no other repo is the right home.

### Apple Developer
- Account is set up + paid (under JBrock dependent, "pending" approval as of 2026-05-03). Once approved, transfer / link to Plainly Digital LLC org.
- Enroll in Apple Small Business Program (15% cut under $1M).
- D-U-N-S verification for org-level account if needed.

### Google Cloud for Startups
- Apply at `cloud.google.com/startup` for the AI Startups track (~$2K credits, possibly higher tier with Anthropic partnership). Plainly Digital qualifies as a pre-revenue startup with multiple GCP-billed projects.
- Once approved, allocate credits across ClearDoc + SitterSheet projects in GCP Console → Billing → Credits.

### Self-hosted CI/CD on GCP (FUTURE)
- Build a private CI/CD pipeline on Google Cloud Build / Cloud Run that all Plainly Digital repos use instead of GitHub Actions minutes. Reduces external dependency, lets us run ZAP / heavyweight scans without Actions runner limits, and keeps build secrets inside our own GCP perimeter.
- Out of scope for v1.

### Trademark search + DBA registration
- "Plainly Digital" trademark search (USPTO TESS). If clean, file ITU. ~$350 filing fee.
- "ClearDoc" + "SitterSheet" trademark searches. Both are crowded namespaces — likely descriptive-mark strategy or alternative naming.
- TN DBA registration if Plainly Digital LLC's articles don't already cover these app names.

### M365 mailbox setup
- `apps@plainlydigital.com` is the single contact across all apps + legal docs. Confirm M365 is delivering reliably (DKIM, SPF, DMARC) before launch.
- DNS records for SPF/DKIM/DMARC need to land in Cloudflare DNS (since the domain moved to Cloudflare nameservers).
