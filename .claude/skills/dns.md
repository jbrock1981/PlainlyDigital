# dns

DNS state inspection + cutover steps for `plainlydigital.com`. Read this when the user asks anything about DNS, nameservers, mail records, or "why isn't the site live yet."

## Current authoritative state (verify, don't assume)

```bash
dig plainlydigital.com NS @8.8.8.8 +short          # returns nameservers Google sees as authoritative
dig plainlydigital.com NS @1.1.1.1 +short          # cross-check via Cloudflare resolver
dig plainlydigital.com SOA +short                   # the SOA record's master NS
```

**Expected post-migration** (after cutover): four `*.googledomains.com.` nameservers from the `plainlydigital-com` Cloud DNS managed zone.

**Pre-migration** (current as of plan write): GoDaddy nameservers (`ns*.domaincontrol.com.`).

If `dig` returns GoDaddy nameservers, the cutover step `A5.6` from the migration plan hasn't happened yet — DO NOT tell the user the migration is complete.

## Inspect Cloud DNS records

```bash
gcloud dns managed-zones list --project=plainlydigital-www
gcloud dns record-sets list --zone=plainlydigital-com --project=plainlydigital-www
gcloud dns record-sets list --zone=plainlydigital-com --project=plainlydigital-www --type=A --name=plainlydigital.com.
```

## DNS cutover order (must run in this exact order)

This is the only step that can break email + the site simultaneously. Do not skip 1–2.

1. **Export GoDaddy DNS export.** GoDaddy → DNS Management → Export → save the zone file. This captures any M365 mail records (DKIM/SPF/DMARC for `apps@plainlydigital.com`), domain verification TXTs, anything else.

2. **Re-create non-parking records in Cloud DNS** before changing nameservers. Specifically:
   - SPF: `v=spf1 include:spf.protection.outlook.com -all` on apex (TXT)
   - DKIM: `selector1._domainkey CNAME selector1-plainlydigital-com._domainkey.<tenant>.onmicrosoft.com.`
   - DKIM: `selector2._domainkey CNAME selector2-plainlydigital-com._domainkey.<tenant>.onmicrosoft.com.`
   - DMARC: `_dmarc TXT "v=DMARC1; p=quarantine; rua=mailto:apps@plainlydigital.com"`
   - MX: `0 plainlydigital-com.mail.protection.outlook.com.`
   - Autodiscover: `autodiscover CNAME autodiscover.outlook.com.`
   - Any `_office365.<domain>` verification TXT (only if M365 is mid-verification)

3. **Add custom domain in Firebase Hosting** for both `plainlydigital.com` and `www.plainlydigital.com` (Firebase Console → Hosting → Add custom domain). Firebase prints the records you need.

4. **Add Firebase records to Cloud DNS** (typically two A on apex, two AAAA, plus TXT verification):
   ```
   plainlydigital.com.    A     <Firebase IP 1>
   plainlydigital.com.    A     <Firebase IP 2>
   plainlydigital.com.    AAAA  <Firebase IPv6 1>
   plainlydigital.com.    AAAA  <Firebase IPv6 2>
   plainlydigital.com.    TXT   "google-site-verification=<token>"
   www.plainlydigital.com. CNAME plainlydigital.web.app.
   ```

5. **Wait for Firebase to verify the TXT.** Since GoDaddy is still authoritative, Firebase will check via the resolver, which still queries GoDaddy. Add the TXT in BOTH GoDaddy AND Cloud DNS for this step (only briefly — remove from GoDaddy after).

6. **Change GoDaddy nameservers** to the four Cloud DNS NS values. GoDaddy: Domain Settings → Nameservers → Change → I'll use my own. Paste the `ns-cloud-X.googledomains.com.` values.

7. **Verify propagation** (most resolvers cut over <1h, max 24h):
   ```bash
   dig plainlydigital.com NS @8.8.8.8 +short
   dig plainlydigital.com A @1.1.1.1 +short
   dig www.plainlydigital.com CNAME @8.8.8.8 +short
   ```

8. **Verify HTTPS** (Firebase auto-provisions Let's Encrypt cert once DNS is authoritative):
   ```bash
   openssl s_client -connect plainlydigital.com:443 -servername plainlydigital.com </dev/null 2>/dev/null | openssl x509 -noout -issuer -dates
   ```

9. **Verify mail still works.** Send test from `apps@plainlydigital.com` to a Gmail and an Outlook recipient. Inspect headers for `dkim=pass spf=pass dmarc=pass`. If any fail, the corresponding record in step 2 is wrong.

## What the migration plan is referencing

If the user mentions "the plan" or "the migration plan" without a path, they mean `C:\Users\jbroc\.claude\plans\we-need-to-move-silly-rose.md`, section A4 (Cloud DNS) and A5 (cutover).

## Verify-before-claim reminder

Never tell the user "DNS is on Cloud DNS" or "the site is live at plainlydigital.com" without running the `dig` checks above first. The user has been burned by this exact assumption — ROADMAP.md line 58 said "DNS migrated to Cloudflare nameservers" for weeks while DNS was actually still at GoDaddy parking.
