# Plainly Digital

Marketing site, legal docs, and parent documentation for **Plainly Digital LLC**.

Live at: https://plainlydigital.com

## What's here

- Public marketing site (Astro + MDX, deployed to Firebase Hosting under GCP project `plainlydigital-www`)
- Privacy policy + ToS for each Plainly Digital app (linked from the apps themselves)
- Parent-company docs

## Apps in the suite

| App | Status | Purpose |
|---|---|---|
| ClearDoc | Pre-launch (mobile) | Snap any document, get plain-English answers |
| SitterSheet | Pre-launch (mobile) | AI-generated pet/house-sitter guide, one shareable link |
| Plainly | Coming soon | Financial literacy for Gen Z |
| Vinla | Coming soon | Health intelligence with N-of-1 experiments |
| Winlet | Coming soon | Daily wins tracker with AI-powered remixes |
| AI Life Advisor | Coming soon | Personal AI advisor for life questions (name TBD) |

## Stack

- Astro 5 + MDX
- Plain CSS with custom properties
- Firebase Hosting (GCP project `plainlydigital-www` under `apps-org`)
- Cloud DNS for `plainlydigital.com` authoritative DNS
- Cloud Build CI/CD on push to `main`
- Zero third-party JS

## Local development

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output to dist/
npm run preview  # preview the built site
```

## Pre-deploy checks

```bash
npm run audit         # npm audit moderate+
npm run lint:links    # linkinator on dist/
npm run lint:a11y     # pa11y-ci WCAG 2.1 AA
npm run lighthouse    # Lighthouse CI
```

## Security disclosure

`apps@plainlydigital.com` — see [`/.well-known/security.txt`](public/.well-known/security.txt).

## License

All content © Plainly Digital LLC. All rights reserved.
