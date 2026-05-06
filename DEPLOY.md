# Deploy + DNS runbook — Plainly Digital marketing site

Operator-facing reference for the Plainly Digital LLC marketing site at `https://plainlydigital.com`. Covers one-time GCP setup, day-2 deploys, DNS cutover, cert renewal, and rollback.

For Claude-facing guidance (skills + hooks), see `CLAUDE.md` and `.claude/skills/`.

---

## Architecture summary

| Layer | What it is |
|---|---|
| Source | `jbrock1981/PlainlyDigital` on GitHub, Astro 5 + MDX |
| Build | Cloud Build via `cloudbuild.yaml` on push to `main` |
| Host | Firebase Hosting, GCP project `plainlydigital-www` (apps-org) |
| DNS | Cloud DNS managed zone `plainlydigital-com` |
| Registrar | GoDaddy (registration only — DNS authority is Cloud DNS) |
| Cert | Let's Encrypt, auto-issued + renewed by Firebase |
| Email | Microsoft 365, mail records live in Cloud DNS alongside web records |

---

## One-time setup (run once, then check off)

These commands assume `gcloud` is authenticated as `apps@plainlydigital.com` and the Cloud Identity org `apps-org` (`611419173109`) is reachable.

### Project + APIs

```bash
gcloud projects create plainlydigital-www --organization=611419173109
gcloud beta billing projects link plainlydigital-www --billing-account=019368-94B72C-5B073A
gcloud config set project plainlydigital-www

gcloud services enable \
  firebasehosting.googleapis.com \
  firebase.googleapis.com \
  dns.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --project=plainlydigital-www
```

### Add Firebase to the project

The `addFirebase` API 403s for this billing account regardless of CLI auth (documented gotcha in `reference_plainly_gcp_billing.md`). Use the Firebase Console:

1. https://console.firebase.google.com → Add project → "Add Firebase to a Google Cloud project"
2. Pick `plainlydigital-www`. Accept Blaze plan if prompted (static hosting won't bill — Spark would also work).
3. After Firebase is added: Console → Hosting → Get started → finish wizard. Default site = project ID.

### Cloud DNS managed zone

```bash
gcloud dns managed-zones create plainlydigital-com \
  --dns-name="plainlydigital.com." \
  --description="Plainly Digital LLC apex" \
  --visibility=public \
  --project=plainlydigital-www

gcloud dns managed-zones describe plainlydigital-com \
  --project=plainlydigital-www \
  --format="value(nameServers)"
```

Capture the four `*.googledomains.com.` nameservers. You'll need them at the GoDaddy step.

### Cloud Build GitHub connection + trigger

```bash
# 1. Connect GitHub (interactive — one-time per host)
gcloud builds connections create github plainlydigital-github \
  --region=us-central1 \
  --project=plainlydigital-www
# Follow the printed URL, install the Cloud Build app on jbrock1981 org, authorize.

# 2. Link the repo
gcloud builds repositories create plainlydigital-www-repo \
  --connection=plainlydigital-github \
  --remote-uri=https://github.com/jbrock1981/PlainlyDigital.git \
  --region=us-central1 \
  --project=plainlydigital-www

# 3. Production trigger on push to main
gcloud builds triggers create github \
  --name=plainlydigital-www-prod \
  --repository=projects/plainlydigital-www/locations/us-central1/connections/plainlydigital-github/repositories/plainlydigital-www-repo \
  --branch-pattern=^main$ \
  --build-config=cloudbuild.yaml \
  --region=us-central1 \
  --project=plainlydigital-www
```

### Cloud Build SA permissions

```bash
PROJECT_NUMBER=$(gcloud projects describe plainlydigital-www --format="value(projectNumber)")
CB_SA="${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com"

gcloud projects add-iam-policy-binding plainlydigital-www \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/firebasehosting.admin"

gcloud projects add-iam-policy-binding plainlydigital-www \
  --member="serviceAccount:${CB_SA}" \
  --role="roles/firebase.admin"
```

---

## DNS cutover (the high-stakes step)

**Run only after** Firebase Hosting is up and the site is verified at `https://plainlydigital.web.app/`.

Sequence matters — wrong order = email outage. Full play-by-play in `.claude/skills/dns.md`. Short version:

1. Export current GoDaddy DNS to capture M365 mail records.
2. Recreate non-parking records (SPF/DKIM/DMARC/MX/Autodiscover) in Cloud DNS.
3. Firebase Console → Hosting → Add custom domain → enter `plainlydigital.com` and `www.plainlydigital.com`. Capture the records Firebase prints.
4. Add Firebase records (A/AAAA/CNAME/TXT) to Cloud DNS.
5. Wait for Firebase to verify the TXT (TXT must exist in current authoritative DNS, which is still GoDaddy — temporarily add TXT to GoDaddy too).
6. GoDaddy → Domain Settings → Nameservers → Change → enter the four `ns-cloud-X.googledomains.com.` values from the managed zone.
7. Verify:
   ```bash
   dig plainlydigital.com NS @8.8.8.8 +short
   dig plainlydigital.com A @1.1.1.1 +short
   dig www.plainlydigital.com CNAME @8.8.8.8 +short
   curl -I https://plainlydigital.com/
   openssl s_client -connect plainlydigital.com:443 -servername plainlydigital.com </dev/null 2>/dev/null | openssl x509 -noout -issuer -dates
   ```
8. Verify mail: send `apps@plainlydigital.com → gmail` and `→ outlook`, check headers for `dkim=pass spf=pass dmarc=pass`.

---

## Day-2 ops

### Deploy

```bash
# normal flow:
git push origin main
gcloud builds list --project=plainlydigital-www --limit=1
# → SUCCESS within ~3 min, Firebase Hosting auto-updates
```

### Preview channel

```bash
firebase use plainlydigital-www
firebase hosting:channel:deploy preview-<slug> --only hosting --expires 7d
firebase hosting:channel:list
```

### Rollback

```bash
firebase use plainlydigital-www
firebase hosting:releases:list --site=plainlydigital-www | head -5
firebase hosting:rollback --site=plainlydigital-www
```

Instant. No DNS change, no cert change.

### Cert renewal

Auto. If the cert lapses (rare — Firebase ACMEs every 60–90 days):
1. Firebase Console → Hosting → Custom domains → `plainlydigital.com` → status will show error
2. Click "Refresh" or remove + re-add the domain
3. Verify with `openssl s_client` after 5–10 minutes

### Cost monitoring

Static hosting under startup credits is rounding error, but check monthly:
```bash
gcloud billing accounts get-iam-policy 019368-94B72C-5B073A   # confirm linkage
# Console → Billing → Reports → filter by project=plainlydigital-www
```

---

## Decommission Cloudflare Pages

After the migration is verified live, work through these in order. Don't skip the 14-day window — it's the safety net.

1. Cloudflare dashboard → Pages → `plainly-digital` (or whatever the project is named) → Settings → pause deployments. Don't delete yet.
2. In this repo: delete `public/_headers` (Firebase Hosting now serves the headers from `firebase.json`).
3. Update `README.md`: remove Cloudflare references, replace with Firebase Hosting.
4. Wait 14 days. If nothing breaks: Cloudflare → delete the Pages project.
5. If a Cloudflare account exists solely for this site (no other PD properties on it), close that account too.

---

## Disaster recovery

| Failure | Recovery |
|---|---|
| Cloud Build broken, prod deploy needed | `firebase use plainlydigital-www && firebase deploy --only hosting` from a clean checkout of `main` |
| Firebase Hosting down (regional) | Cloudflare Pages project is paused for 14 days post-cutover; un-pause + revert GoDaddy nameservers to fall back |
| Cloud DNS deleted/corrupted | Cloud DNS export was captured during cutover; restore from `gcloud dns record-sets import`. If catastrophic: revert GoDaddy nameservers + recreate zone from export |
| GCP project deleted | 30-day soft delete window: `gcloud projects undelete plainlydigital-www`. Past 30 days: rebuild from this runbook |
| Custom domain stuck "needs verification" | Firebase Console → remove + re-add domain; check the TXT propagated with `dig _firebase-hosting.plainlydigital.com TXT @8.8.8.8` |

---

## What NOT to do

- Don't run `gcloud projects delete plainlydigital-www` — you'd kill DNS authority simultaneously with hosting. Settings.json deny-lists this.
- Don't delete the Cloud DNS managed zone before nameservers are reverted at GoDaddy — that's a real outage.
- Don't `firebase deploy --only firestore` or `--only functions`. The site has neither.
- Don't push to `main` with broken local build. The pre-commit hook tries to catch this; bypassing it just shifts the failure to Cloud Build a few minutes later.
- Don't merge a PR without verifying preview channel renders the affected pages.
