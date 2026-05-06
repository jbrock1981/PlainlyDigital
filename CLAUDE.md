# Plainly Digital — marketing site

## What this is

Static marketing + legal-docs site for **Plainly Digital LLC** at `https://plainlydigital.com`. Astro 5 + MDX, hosted on **Firebase Hosting** under GCP project `plainlydigital-www` (apps-org, billing `019368-94B72C-5B073A`). Authoritative DNS lives in **Cloud DNS**. CI/CD runs through **Cloud Build** on push to `main` (no GitHub Actions deploy).

The site holds privacy policy + ToS for every Plainly Digital app (ClearDoc, SitterSheet, Plainly, Vytally, Accomplishly, AI Life Advisor) plus the parent-LLC about/landing pages.

## The bar for this repo

Produce functional, accurate work on the first pass. The error class this CLAUDE.md is designed to prevent is **claiming infra state without verifying it** — e.g., saying "the site is on GCP" when it's actually on Cloudflare Pages, or "DNS is on Cloudflare" when it's still at GoDaddy. Read the file, run the command, then answer.

## Verify-before-claim rules

Before stating that any infra X exists or is in state Y, run the command that proves it. Memory and ROADMAP.md are point-in-time snapshots and may be stale.

| Question | Authoritative source — DO use this | Stale source — DON'T trust this alone |
|---|---|---|
| Where is the site hosted? | `firebase.json` + `.firebaserc` | memory entries, ROADMAP.md, README.md |
| What's the GCP project? | `cat .firebaserc` | memory |
| What deploy ran last? | `gcloud builds list --project=plainlydigital-www --limit=5` | memory |
| What does DNS resolve to right now? | `dig plainlydigital.com @8.8.8.8` and `@1.1.1.1` | any doc that says "we're on X" |
| Are nameservers on Cloud DNS yet? | `dig plainlydigital.com NS +short` | ROADMAP.md (line 58 was wrong for weeks) |
| Is the cert valid? | `openssl s_client -connect plainlydigital.com:443 </dev/null \| openssl x509 -noout -issuer -dates` | console screenshots |

If memory and the live config disagree, **the live config wins** and you must update memory in the same session.

## Edit discipline

- **Never `Write` an existing tracked file.** Always `Edit`. Writing an existing file risks truncation. The repo-level Write hook will warn on >50% line shrink, but don't rely on it as a safety net — use Edit.
- **Read before edit.** Edit refuses to operate without a prior Read; do not try to skip this.
- **Verify working directory before edits.** Confirm `pwd` matches `C:\Users\jbroc\PlainlyDigital\` before any change. Cross-repo edits are a frequent error class — file paths in this repo collide with similar names in ClearDoc, SitterSheet, etc.

## Build before commit

If your change touches `*.astro`, `*.mdx`, `*.ts`, `*.tsx`, `*.json`, `*.css`, or `astro.config.mjs`, run a clean build before committing:

```bash
npm ci         # only if package-lock changed
npm run build  # must exit 0
```

A pre-commit hook enforces this. If the hook is bypassed (don't), the build fails on Cloud Build and the deploy is blocked.

## Functional verification

For non-trivial changes (new page, layout edit, header/CSP change), serve the build and load the affected page in a browser:

```bash
npm run preview   # http://localhost:4321 (or :4322 if 4321 is busy)
```

For header changes specifically (CSP, HSTS, COOP, etc.) verify with:
```bash
curl -I http://localhost:4321/
```

For external (post-deploy) verification, use:
```bash
curl -I https://plainlydigital.web.app/         # Firebase preview URL (always live)
curl -I https://plainlydigital.com/                 # production after DNS cutover
```

## Pre-deploy checklist

Run all four before any production deploy. The Cloud Build trigger runs the first three automatically; running them locally first means you catch failures without a wasted build minute.

```bash
npm run audit         # npm audit --audit-level=high — must exit 0
npm run build         # Astro build — must exit 0
npm run lint:links    # linkinator — no broken internal links
npm run lighthouse    # Lighthouse CI — perf >=0.9, a11y =1.0, SEO >=0.95
```

Once the GCP CI/CD pipeline (in ROADMAP.md as "Self-hosted CI/CD on GCP") is built, these gates move into Cloud Build pre-deploy steps for every PR.

## Key paths

- `src/pages/` — 14 routes total (8 Astro, 6 MDX). Top-level: `index`, `about`, `privacy`, `terms`. Per-app subdirs: `cleardoc/{index,privacy,terms}`, `sittersheet/{index,privacy,terms}`, plus coming-soon stubs for `plainly/`, `vytally/`, `accomplishly/`, `ai-life-advisor/`.
- `src/layouts/` — `BaseLayout`, `LegalLayout`, `ComingSoonLayout`
- `src/components/` — `Header`, `Footer`, `Hero`, `AppCard`, `PhoneMockup`, `Disclaimer`
- `src/data/apps.ts` — single source of truth for app metadata + slug lookup
- `src/styles/` — `tokens.css`, `global.css`
- `firebase.json` — Firebase Hosting config: security headers (HSTS/CSP/X-Frame-Options/Referrer-Policy/Permissions-Policy/COOP/CORP), cache rules, and project link. Authoritative source for headers.
- `cloudbuild.yaml` — Cloud Build pipeline
- `DEPLOY.md` — operator runbook
- `ROADMAP.md` — post-v1 work + LLC operations tracker

## Memory contract

This repo's `firebase.json` + `.firebaserc` + `cloudbuild.yaml` are the canonical source for hosting state. The memory entry `project_plainlydigital_site.md` exists to point future sessions AT those files; it does NOT itself describe deploy state in detail (that would rot).

When you learn something about deployed state in a session, update **both** the memory entry **and** the canonical config in the same session. Never just memory.

## Build & test commands

```bash
npm install                # full install (use ci in CI)
npm ci                     # clean install from lockfile
npm run dev                # localhost:4321 watch mode
npm run build              # static output to dist/
npm run preview            # serve dist/
npm run audit              # npm audit --audit-level=high
npm run audit:full         # npm audit --audit-level=moderate
npm run lint:links         # linkinator dist/
npm run lighthouse         # Lighthouse CI
npm run icons:build        # regenerate PNG icons from SVGs
```

## Deploy

Cloud Build trigger on push to `main` deploys to production. Manual deploy to a preview channel:

```bash
firebase use plainlydigital-www
firebase hosting:channel:deploy preview-<name> --only hosting
```

Full operator runbook including DNS, cert renewal, and rollback: see `DEPLOY.md`.

## Rules

1. All work goes to `main` — no feature branches unless asked.
2. Cloudflare Pages was the pre-migration host (2026-05-04 scaffold deploy only, never resolved at the apex domain). Decommissioned 2026-05-06. Don't reference it as live.
3. Never reference vendors like Anthropic/OpenAI in customer-facing copy on this site (the apps don't, the marketing site shouldn't either).
4. Privacy/ToS MDX files cite Tennessee governing law — keep this consistent across all per-app legal docs.
5. Zero third-party JS. No analytics, no fonts loaded from Google, no embedded scripts. Privacy-preserving cookieless analytics may be added per ROADMAP v1.x.

## Current priority

GCP migration of the marketing site is COMPLETE (plan: `C:\Users\jbroc\.claude\plans\we-need-to-move-silly-rose.md`). Production traffic hits Firebase Hosting under `plainlydigital-www`. DNS authoritative on Cloud DNS (`plainlydigital-com` zone). Apex + www both serve from Firebase with Google Trust Services SSL.
