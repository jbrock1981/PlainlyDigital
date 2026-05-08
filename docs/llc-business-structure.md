# LLC Business Structure — Plainly Digital LLC

## Overview

This document covers the legal and business structure for operating
multiple apps and services under a single LLC entity.

---

## Registered Entity

| Field | Value |
|---|---|
| **Legal Name** | PLAINLY DIGITAL LLC |
| **EIN** | 41-4877857 |
| **Entity Type** | Single-Member LLC |
| **State of Formation** | Tennessee |
| **County** | Giles |
| **Registered Address** | 1309 Case Rd, Prospect TN 38477 |
| **Phone** | 256-694-5266 |
| **Responsible Party** | Jonathan Brock (Sole Member) |
| **TN SOS Tracking #** | B2026241384 |
| **TN SOS Control #** | 002094776 |
| **Formation Date** | March 2026 |
| **Principal Activity** | Digital Applications & Technology Consulting |

---

## Structure: Single Parent LLC (Studio Model)

**Purpose:** Umbrella entity that owns, operates, and generates revenue from all products

One LLC:
- Keeps overhead low (one registered agent, one tax filing, one bank account)
- Avoids the complexity of subsidiary management
- Can be restructured into a holding company later if one product scales significantly
- Uses DBA (Doing Business As) registrations for each brand name

```
PLAINLY DIGITAL LLC  ←  parent legal entity
    │
    ├── Plainly          (DBA — financial literacy app for Gen Z)
    ├── Vytally          (DBA — personal health intelligence app)
    └── Advisedly        (DBA — AI-augmented cybersecurity compliance consulting)
```

> **Note on Advisedly:** Consulting carries higher professional liability risk than consumer
> apps. Consider spinning Advisedly into its own LLC before signing the first paying client
> engagement. DBA is fine for pre-revenue activity (partner applications, setup, etc.).

---

## LLC Name

**Plainly Digital LLC** is the parent studio entity for all products in the portfolio.
Each brand (Plainly, Vytally, Advisedly) operates as a DBA under this entity.

Registering each name as a DBA (also called a "trade name" or "assumed name") in
Tennessee lets you open bank accounts, sign contracts, and accept payments under each
brand while the legal entity remains Plainly Digital LLC.

**Registered DBAs (pending TN SOS filing):**
- **Plainly** — financial literacy app
- **Vytally** — personal health intelligence app
- **Advisedly** — AI-augmented cybersecurity compliance consulting

---

## The Product Portfolio

### 1. Plainly — Financial Literacy App
- **Target:** Ages 18–28, Gen Z entering financial adulthood
- **Core:** Bite-sized lessons + AI coach (Claude) + Plaid bank connection
- **Revenue model:** Freemium subscription (~$8–12/month for premium)
- **Repo:** `jbrock1981/Claude-`
- **Key legal considerations:**
  - Not a registered investment advisor — never recommend specific securities
  - Not a bank — never hold user funds
  - Plaid integration requires clear privacy disclosures
  - Required disclaimers: "Not financial advice" in coach responses and app

### 2. Vytally — Personal Health Intelligence App
- **Target:** Ages 18–28, health-conscious Gen Z users
- **Core:** Logging (food, water, exercise, sleep) + AI-powered insights + trends
- **Revenue model:** Freemium subscription (~$9.99/month)
- **Repo:** `jbrock1981/health-ai`
- **Key legal considerations:**
  - **Not a medical device or healthcare provider** — must be explicit
  - HIPAA does NOT apply to wellness apps that aren't covered entities
  - Health data is sensitive — robust privacy policy required
  - FDA guidance: general wellness apps are low-risk if no diagnostic claims are made
  - Required disclaimers: "Not medical advice" in AI responses; consult a doctor

### 3. Advisedly — AI-Augmented Compliance Consulting
- **Target:** Small-to-mid-sized defense contractors needing CMMC/NIST 800-171 compliance
- **Core:** CMMC Level 2 readiness, RMF/ATO packages, virtual ISSO services
- **Revenue model:** Project-based and retainer consulting fees
- **Repo:** `jbrock1981/Advisedly`
- **Key legal considerations:**
  - Professional liability (E&O) — clients can sue if assessments are wrong
  - Contracts must clearly scope deliverables and limit liability
  - Consider separate LLC before first paying engagement
  - Microsoft 365 GCC High recommended for CMMC compliance optics with DoD clients

---

## Regulatory & Compliance Matrix

| Product | Data Type | Key Regulation | What You Must Do |
|---|---|---|---|
| Plainly | Bank/financial data | Plaid TOS, state money transmission laws | Don't hold funds; "not financial advice" |
| Vytally | Health/biometric data | FTC Act, state privacy laws | Strong privacy policy; no diagnostic claims |
| Advisedly | Client CUI/compliance data | CMMC, NIST 800-171, DFARS | Handle client data per contractual requirements |
| All | Personal data | COPPA (if under 13), CCPA (California) | Age gate at 13+; honor deletion requests |

---

## Setup Sequence: DBA → Domain → Email

This is the correct order. Each step depends on the previous one.

### Step 1 — Register DBAs in Tennessee (~$20/name, 10 min each)
Go to **tnsos.gov** → Business Services → Trade Name Registration.
File under Plainly Digital LLC EIN (41-4877857). Register:
- `Plainly`
- `Vytally`
- `Advisedly`

### Step 2 — Register Domains (can do simultaneously with DBAs)

| Brand | Primary Domain | Alternatives |
|---|---|---|
| Advisedly | `advisedly.ai` | `advisedly.com` |
| Vytally | `vytally.com` | `vytally.health`, `vytally.app` |
| Plainly | `plainly.app` | `getplainly.com` |

Register at Namecheap or Google Domains (~$10–15/year each). Also claim matching
social handles (Instagram, TikTok, X) even if not yet active — establishes prior use.

### Step 3 — Set Up Business Email (after domains are live, ~1 hour)

| Brand | Recommended | Cost | When |
|---|---|---|---|
| Advisedly | Google Workspace on `advisedly.ai` | ~$6/mo | Now (needed for partner portals) |
| Advisedly (long-term) | Microsoft 365 GCC High | ~$57/user/mo | Before first DoD-adjacent client |
| Vytally / Plainly | Google Workspace on their domains | ~$6/mo | Before public launch |

Use `jonathan@advisedly.ai` (or similar) for the Anthropic Claude Partner Portal application.

---

## GitHub Organization Migration Plan

**Target structure:** Move all repos into a `PlainlyDigital` GitHub Organization so
everything lives under one company account instead of a personal account.

```
github.com/PlainlyDigital/
  ├── business      (LLC docs, legal, roadmaps — contents of this repo)
  ├── vytally       (health app — currently jbrock1981/health-ai)
  ├── plainly       (finlit app — currently jbrock1981/Plainly)
  └── advisedly     (consulting — currently jbrock1981/Advisedly)
```

**Cost:** Free for public repos. $4/user/month for private repos (GitHub Team plan).
All four repos should be private until public launch — budget ~$4–8/month.

**Migration steps (do when ready to go public or onboard collaborators):**
1. Create `PlainlyDigital` organization at github.com/organizations/new
2. Transfer each repo: repo Settings → Danger Zone → Transfer ownership → PlainlyDigital
3. Rename repos on transfer: `health-ai` → `vytally`, `Claude-` → `business`, etc.
4. Update any Vercel / CI links that reference the old repo paths
5. Update README cross-links between repos

**Current state (pre-org, personal account):**

| Final Name | Current Repo | Status |
|---|---|---|
| `PlainlyDigital/business` | `jbrock1981/Claude-` | Business docs live here |
| `PlainlyDigital/plainly` | `jbrock1981/Plainly` | App code moved here ✓ |
| `PlainlyDigital/vytally` | `jbrock1981/health-ai` | In private beta |
| `PlainlyDigital/advisedly` | `jbrock1981/Advisedly` | Active |

---

## Operating Agreement Provisions to Include

Even as a single-member LLC, write an operating agreement that addresses:

1. **Product ownership clause** — all products, code, IP developed under the LLC are
   assets of the LLC
2. **Revenue allocation** — if you bring on co-founders per product, specify allocation
3. **IP assignment** — contractors must sign IP assignment agreements
4. **Future subsidiaries** — include language allowing the LLC to form wholly-owned
   subsidiaries if a product reaches scale warranting separation

---

## Banking & Financial Setup

| Account | Purpose |
|---|---|
| Main LLC business checking | Operating expenses |
| Advisedly sub-account | Consulting revenue |
| Vytally sub-account | App subscription revenue |
| Plainly sub-account | App subscription revenue |
| LLC savings/reserve | 3-month operating reserve |

Mercury (mercury.com) allows sub-accounts under one LLC — recommended.

---

## Tax Structure

- **Default LLC taxation:** Pass-through to personal return (Schedule C)
- **S-Corp election:** Consider once net profit exceeds $60–80k/year
- **Track expenses per product:** Use accounting categories in Wave or QuickBooks

---

## Launch Checklist

### Entity Setup
- [x] Form LLC in Tennessee — initially as CLEARPATH DIGITAL LLC
- [x] Get EIN from IRS — EIN: 41-4877857
- [x] File Articles of Amendment — renamed to PLAINLY DIGITAL LLC (Control # 002094776)
- [ ] Register DBA — "Plainly" in Tennessee (tnsos.gov)
- [ ] Register DBA — "Vytally" in Tennessee (tnsos.gov)
- [x] Register DBA — "Advisedly" in Tennessee (tnsos.gov)
- [ ] Register DBA — "Plainly" in Tennessee (tnsos.gov)
- [ ] Register DBA — "Vytally" in Tennessee (tnsos.gov)
- [ ] **FILE NOW: FinCEN BOI report** — fincen.gov/boi, required within 90 days of LLC formation, civil/criminal penalties for non-compliance
- [ ] Sign and execute LLC Operating Agreement (draft in `legal/01_LLC_Operating_Agreement.docx`)
- [ ] Obtain Giles County local business license (~$15/year)
- [ ] Open business bank account (Mercury recommended — mercury.com)
- [ ] Set up accounting (Wave free, or QuickBooks Simple Start $30/mo)

### Domains & Identity
- [x] Register `advisedly.ai` — purchased via GoDaddy
- [ ] Register `vytally.com` (and `.health` or `.app`)
- [ ] Register `plainly.app` (or `getplainly.com`)
- [ ] Claim social handles for all three brands (Instagram, TikTok, X)
- [x] Set up Microsoft 365 Business Standard on `advisedly.ai` — `jbrock@advisedly.ai`

### Trademarks
- [x] Search USPTO TESS for "Plainly" — clear in Class 009 & 042
- [x] Search USPTO TESS for "Vytally" — completely clear
- [ ] Search USPTO TESS for "Advisedly"
- [ ] File ITU trademark for "Plainly" — Class 042 (~$350), Class 009 at launch (~$350)
- [ ] File ITU trademark for "Vytally" — Class 042 (~$350), Class 009 at launch (~$350)
- [ ] File Statement of Use for each mark after launch (~$100/class)

### Advisedly Consulting Launch
- [x] Advisedly business plan drafted — see `jbrock1981/Advisedly` repo
- [x] Register DBA "Advisedly" in Tennessee
- [x] Register `advisedly.ai` domain (GoDaddy)
- [x] Landing page live at advisedly.ai (Vercel)
- [x] Set up Microsoft 365 Business Standard — `jbrock@advisedly.ai`
- [x] Apply to Anthropic Claude Partner Network
- [ ] **FILE NOW: FinCEN Beneficial Ownership Information (BOI) report** — fincen.gov/boi, ~10 min, due within 90 days of LLC formation date
- [ ] Obtain Giles County business license (~$15/year)
- [ ] Sign and date LLC Operating Agreement as sole member (execute the draft in `legal/`)
- [ ] Attorney review of MSA, SOW, and all `legal/` documents before client use
- [ ] Get E&O (professional liability) insurance quote — Hiscox or Embroker (before first client)
- [ ] Draft Advisedly website Terms of Service and Privacy Policy
- [ ] Consider forming Advisedly LLC (separate from Plainly Digital) before first engagement
- [ ] Upgrade to Microsoft 365 GCC High (before handling client CUI)

### Plainly App Launch
- [ ] Add Plaid integration
- [ ] Add authentication (Clerk or Supabase)
- [ ] Build individual lesson screens
- [ ] Attorney review of privacy policy and ToS (`legal/` folder)
- [ ] Add "Powered by Claude" to App Store listing description
- [ ] Complete Apple App Store Privacy Nutrition Label

### Vytally App Launch
- [x] App built and in private beta (`jbrock1981/health-ai`)
- [x] Privacy policy and ToS drafted (`jbrock1981/Claude-/legal/`)
- [x] "AI-generated · Not medical advice" label on all AI responses
- [ ] Attorney review of privacy policy and ToS before public launch
- [ ] Add "Powered by Claude" to App Store listing description
- [ ] Complete Apple App Store Privacy Nutrition Label
- [ ] Add explicit AI consent step to onboarding

### Anthropic API Compliance
- [x] "Not financial advice" / "not medical advice" disclaimers in system prompts
- [x] Anthropic listed as data processor in privacy policy drafts
- [x] API cost model documented — see `docs/api-cost-model.md`
- [ ] Save copy of Anthropic API ToS and Privacy Policy to business records
- [ ] Confirm no-training setting active at console.anthropic.com

---

## Trademark Protection

> A DBA and website do NOT protect your brand name. Someone can file a trademark on
> your DBA name, forcing you to rebrand. Federal trademark registration is the only
> reliable protection.

File ITU (Intent to Use) applications as soon as brands are in active development —
this locks in your priority date before launch.

**Budget:** ~$700–$1,400 per brand (two classes each), or ~$2,100–$4,200 for all three brands.
Consider prioritizing Advisedly and Vytally first (most distinctive; least likely USPTO challenge).

---

## When to Separate Into Subsidiary LLCs

| Trigger | Action |
|---|---|
| Advisedly signs first paying client | Strong signal to form Advisedly LLC now |
| Any single product hits $500k revenue | Spin that product into its own LLC |
| Outside investor for one product | Separate LLC required for clean equity |
| Co-founder on one product only | Separate LLC for clean ownership |

---

## Recommended Tools

| Need | Tool |
|---|---|
| DBA registration | tnsos.gov (Tennessee SOS website) |
| Domain registration | Namecheap or Google Domains |
| Business email | Google Workspace (~$6/mo) |
| Business banking | Mercury (no fees, API-friendly) |
| Accounting | Wave (free) or QuickBooks Simple Start |
| Contracts / IP assignment | Clerky or a startup attorney |
| Trademark filing | Trademark Engine or a trademark attorney |
| E&O Insurance (Advisedly) | Hiscox or Embroker (online quotes) |

---

*Last updated: March 2026*
*This document is for planning purposes only and is not legal advice.
Consult a licensed attorney for your specific situation.*
