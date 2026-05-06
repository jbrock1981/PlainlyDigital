# deploy

Pre-deploy + deploy + post-deploy runbook for the Plainly Digital marketing site. Read this in full when the user asks to deploy, ship, push to prod, or cut a release. The full operator-facing version with one-time setup is `DEPLOY.md` at repo root.

## When to use this skill

- User says: "deploy", "ship it", "push to prod", "cut a release", "deploy a preview"
- User asks about hosting state, cert, or post-deploy verification
- A Cloud Build run failed and we're triaging

## Pre-flight (always)

Run these in order. Each must exit clean before proceeding. If any step fails, fix the failure — do not bypass.

```bash
git status                                   # working tree must be clean
git branch --show-current                    # confirm intended branch
npm ci                                       # only if package-lock changed since last build
npm run audit                                # npm audit --audit-level=high → exit 0
npm run build                                # must produce dist/
npm run lint:links                           # linkinator on dist/ → no broken internal links
npm run lighthouse                           # perf >=0.9, a11y =1.0, SEO >=0.95
```

## Production deploy

Production deploys happen via Cloud Build trigger on push to `main`. You almost never run `firebase deploy` manually for production:

```bash
git push origin main
gcloud builds list --project=plainlydigital-www --limit=1
gcloud builds log <BUILD_ID> --project=plainlydigital-www  # if you need to see the run
```

If Cloud Build is disabled or unavailable and the user explicitly asks for a manual production deploy:

```bash
firebase use plainlydigital-www
firebase deploy --only hosting --message "manual deploy <reason>"
```

## Preview channel deploy

For PRs and ad-hoc previews:

```bash
firebase use plainlydigital-www
firebase hosting:channel:deploy preview-<slug> --only hosting --expires 7d
firebase hosting:channel:list                        # shows the temporary URL
```

The preview URL is `https://plainlydigital-www--preview-<slug>-<hash>.web.app`. Share that, not the prod URL.

## Post-deploy verification

After ANY deploy (production or preview), do all of these. Don't skip — header regressions are the most common silent breakage.

```bash
URL="https://plainlydigital-www.web.app"   # for production, after DNS cutover use https://plainlydigital.com

# 1. Site responds 200
curl -sI "$URL/" | head -1

# 2. All security headers present
curl -sI "$URL/" | grep -E "^(strict-transport-security|content-security-policy|x-content-type-options|x-frame-options|referrer-policy|permissions-policy|cross-origin-opener-policy|cross-origin-resource-policy):"

# 3. Spot-check critical pages (200)
for path in / /about /privacy /terms /cleardoc/privacy /sittersheet/terms /.well-known/security.txt; do
  echo "$path: $(curl -sI "$URL$path" | head -1)"
done

# 4. Cache headers correct on hashed assets
curl -sI "$URL/_astro/" | grep -i cache-control     # expect max-age=31536000, immutable

# 5. (Production only) cert valid
openssl s_client -connect plainlydigital.com:443 -servername plainlydigital.com </dev/null 2>/dev/null | openssl x509 -noout -issuer -dates
```

## Rollback

Cloud Build deploys are versioned in Firebase Hosting. To roll back:

```bash
firebase use plainlydigital-www
firebase hosting:releases:list --site=plainlydigital-www | head -5
firebase hosting:rollback --site=plainlydigital-www
```

Rollback is instant — no DNS change, no cert change, no waiting.

## What to do when something is broken

| Symptom | First check | Likely cause |
|---|---|---|
| Cloud Build red | `gcloud builds log <id> --project=plainlydigital-www` | local `npm run build` would fail too — reproduce locally |
| Pages 404 in prod, 200 in preview | `firebase.json` `cleanUrls`/`trailingSlash` | mismatch with Astro `build.format: "directory"` |
| CSP blocking something | browser console | update `firebase.json` `Content-Security-Policy` header (don't add inline scripts, find a CSP-compatible alternative) |
| Cert lapsed | `openssl s_client` issuer | Firebase auto-renews; if it failed, re-add the custom domain to retrigger ACME |
| DNS doesn't resolve | `dig plainlydigital.com NS @8.8.8.8` | nameservers aren't pointing at Cloud DNS — see `dns` skill |

## Verify-before-claim reminder

Before telling the user "the deploy succeeded" or "the site is up," actually run the curl + cert checks above. Don't quote a Cloud Build "SUCCESS" status as proof the site works — Cloud Build success only proves the build artifact uploaded; it doesn't prove the response is correct.
