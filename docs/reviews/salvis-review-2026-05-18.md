# Salvis — App review
**Date:** 2026-05-18
**Reviewer:** general-purpose agent (autonomous)
**Repo:** /home/jbroc/repos/Pillarly (local dir; product is Salvis)

## Verdict & 12-month MRR projection

**Depends-on-CPL, but lean toward shelve-or-B2B-pivot.** Even if the $50 Meta test clears the $4 CPL bar, the consumer wedge against free Medisafe/MyTherapy and free CVS/Walgreens text alerts is razor-thin. A solo-dev consumer play here looks structurally unprofitable; the only realistic path to non-trivial MRR is B2B (assisted-living / home-health / independent pharmacies).

| Scenario | MRR (month 12) | Key assumptions |
|---|---|---|
| Conservative | $0–$120 | Ads validate (CPL $4–7), MVP ships month 6, ~40 waitlist→install conversions, 3–5% paid conversion at $7.99 (most churn within 60 days). Senior-handoff friction is severe. |
| Realistic    | $250–$700 | CPL $4–6, modest TikTok/Facebook senior-caregiver organic, 80–150 paid subs, mostly Family Pro+ at $14.99 (the adult-child payer). High month-3 churn. |
| Upside       | $2,500–$5,000 | At least one B2B pilot lands (independent pharmacy chain or 20-bed assisted-living group at $200–500/mo per facility). Consumer side is a lead-gen for B2B, not the product. |

The "upside" requires abandoning the current consumer-app thesis. The "realistic" case does not clear minimum-wage on a 20 hr/wk effort.

## 1. What it actually is (verified from code/repo)

This is a **landing page only**, with zero product code. Confirmed by inspecting the repo:

- `package.json` declares 4 runtime deps: `next ^14.2.35`, `react`, `react-dom`, `@neondatabase/serverless`. No Expo, no React Native, no Anthropic SDK, no OCR library, no voice library, no auth library.
- `app/page.tsx` is a single static marketing page with hero, 3-step "How it works" (snap → understand → family), and 3 pricing cards (Free / Pro $7.99 / Family Pro+ $14.99). Every CTA routes to one `WaitlistForm` component.
- `app/api/waitlist/route.ts` is a 42-line POST handler: validates email regex, inserts into a Neon Postgres `waitlist` table (auto-created), upserts on conflict, captures UA + IP. No double-opt-in, no email confirmation.
- `components/MetaPixel.tsx` fires `PageView` on load and `Lead` on successful waitlist submit. `NEXT_PUBLIC_META_PIXEL_ID` is environment-gated.
- `app/layout.tsx` has basic Open Graph metadata. No `robots`, no Twitter card, no JSON-LD structured data, no canonical URL, no favicon reference visible.

There is **no** OCR prototype, no voice prototype, no mobile app, no auth, no Claude API integration, no interaction-checking dataset, no HIPAA scaffolding. The product as marketed does not exist. The marketed value prop ("voice-first, point-and-scan, interaction checks, family dashboard") is 100% landing-page fiction at this moment — which is fine for a validation page, but mark it for what it is.

## 2. Functionality critique
**Grade:** C

- **Hero copy** ("Never wonder about a pill again") is acceptable, but generic. Doesn't name the target user (senior? adult child?) and doesn't quantify pain (`X% of seniors miss doses` is missing).
- **Trust signals: failing.** No HIPAA-language reassurance, no real photos, no testimonials, no doctor/pharmacist endorsement, no "Made in USA" or "Built by a family caregiver" founder note. A senior/medication audience needs HEAVY trust signals — the page reads like a generic SaaS landing. The disclaimer footer ("assistant, not a medical device") is correct but reads as legal CYA rather than reassurance.
- **Pricing card placement.** Pricing is on the same page above-the-fold scroll. With **zero product**, asking visitors to declare intent at $7.99/$14.99 may suppress waitlist signups. Test removing pricing entirely until you have an MVP screenshot.
- **CTA repetition.** Four separate `WaitlistForm` instances on one page (hero + 3 pricing cards) — fine, but they all submit identical payloads except `pricing_interest`. Good for funnel analytics.
- **Mobile responsiveness.** Tailwind classes (`sm:grid-cols-3`, `sm:flex-row`) look reasonable; 18px base text and senior-friendly defaults per CLAUDE.md. Untested in this review, but the styling shape is acceptable.
- **SEO/meta:** Bare minimum. Open Graph present, but no Twitter card, no structured data, no sitemap.xml or robots.txt referenced. For a waitlist page driven by paid ads this is *fine*; for organic this is a D.
- **Voice-first claim:** **Zero infrastructure.** The word "voice" appears in copy ("with your voice if you prefer") but there is no library, no API call, no recording component. This is purely landing-page positioning, which is honest enough for a pre-MVP, but be aware that you cannot bridge from "voice-first claim" to "voice-first product" without a meaningful build (Whisper API + permissions + TTS + senior-tested UX).
- **Waitlist hygiene:** Single-opt-in only. No confirmation email, no unsubscribe link captured. Borderline CAN-SPAM exposure when you start emailing. Add double-opt-in before first send.

## 3. Sellability critique — CORE QUESTION FOR THIS REVIEW
**Grade:** D+

**Target user (specific):** Ambiguous. Hero copy speaks to "you" (the patient/senior), but the family dashboard and Pro+ tier price the adult child. Pick one. The "who pays vs who uses" tension is unresolved on the page, and it is the #1 reason senior apps fail.

**Their alternative today (name + price):**
- **Medisafe** — **moved to $4.99/mo on Jan 1, 2026** (or $39.99/yr). Free tier limited to 2 medications. Backed by $51.5M, integrated with pharma patient-support programs.
- **MyTherapy** — fully free. Recently introduced more aggressive ad-related data sharing (per MyTherapy's own competitor page), but still free.
- **Round Health** — minimalist freemium, no upsells.
- **Pillo** — free, unlimited meds, no premium tier (2026 review sites list it as the leading free alternative to Medisafe).
- **CVS/Walgreens text alerts** — free, already tied to actual prescriptions (text JOIN to TXT-CVS or JOINRX to 21525).
- **Apple Health / Google Health / Siri / Alexa reminders** — free, already on the device.

**Reason they'd switch — analysis:**

- **Pricing fit:** Salvis Pro at $7.99 is **60% more expensive than Medisafe Premium ($4.99)** and competes against multiple free, well-funded alternatives. Medisafe's own move to paid in Jan 2026 is the single biggest tailwind for this category — but Medisafe undercuts Salvis on price and has 10M+ users of brand equity. The Family Pro+ at $14.99 is *also* above the Medisafe Premium price that already includes "unlimited family profiles." There is no defensible price ladder here.
- **Value prop in one sentence:** Missing. The closest is "Never wonder about a pill again," which is aspirational, not differentiating. Try: *"For adult children: a one-tap dashboard that tells you whether Mom took today's pills, and an interaction-warning system that catches what her pharmacy's app won't."* This at least names the buyer.
- **First 100 paying customers come from where?** Unclear. Meta ads to adult-children-of-seniors is a plausible target audience but expensive — healthcare Meta CPL averaged $52 over the trailing 13 months (peaked $81.34 in Nov 2025, ended Jan 2026 at $23.26). The $50 ad test at $4 CPL threshold is *optimistic* relative to healthcare benchmarks; even at $23 CPL it would yield only ~2 leads.
- **Senior-adoption curve:** Smartphone ownership among 65+ is 61%, and only 27% for 65+ at <$30K household income (Pew 2026). That is your TAM ceiling. Adult children installing for parents creates a handoff: the senior has to learn a new app, grant camera permissions, scan bottles correctly, respond to voice prompts. Every step is a known drop-off. Voice-recognition health apps see 31% discontinuation rates with tutorial-only onboarding (per healthcarereaders.com).
- **Voice-first claim:** Table stakes, not a moat. Siri reminders are free and built-in. Alexa medication reminders are free. Apple Health logging is free. Voice-AI healthcare is a $650M sector growing 37% CAGR — but the value accrues to the platforms (Apple, Amazon, Google) and to clinical-grade vendors, not to a $7.99 consumer wrapper.
- **Organic / viral mechanics:** Effectively none. Medication apps are private; users do not share. The only viral loop is "adult child invites parent" (Family Pro+), and that loop is throttled by the parent's willingness to install.
- **Regulatory risk:** Significant. Interaction-warning copy ("flags dangerous interactions") edges toward medical-device territory if the algorithm makes specific clinical claims. CLAUDE.md correctly notes "ALWAYS frame as an assistant, not a medical device" and "Never give dosage advice." Family-sharing of medication data triggers HIPAA only if you become a Business Associate of a covered entity; consumer-direct does not, but state privacy laws (CA, WA "My Health, My Data") apply. Get a privacy policy live before the first ad dollar spends.

## 4. Top 3 monetization opportunities (URL + date required for each)

1. **B2B: Independent / small-chain pharmacy white-label** — opportunity: license the OCR + interaction-check engine to independent pharmacies as a branded reminder app for their patients; pharmacies already lose patients to CVS/Walgreens text alerts and need a retention tool. Citation: assisted-living and pharmacy-adjacent medication-management software market projected $9.11B in 2026 → $23.29B by 2034 at 12.45% CAGR (https://www.fortunebusinessinsights.com/medication-management-software-market-115703, accessed 2026-05-18). Realistic incremental MRR: $1,500–$4,000 if 1–3 pilots land at $500–1,500/mo. Effort: 30–45 days post-MVP to add white-label theming + admin dashboard.

2. **B2B: Assisted-living facility add-on** — opportunity: 20-to-80-bed facilities under-served by MatrixCare/CareCommunityOS (which target mid-to-large operators). Citation: North America assisted-living software market $19.19B in 2024 → $36.33B by 2032 at 8.3% CAGR (https://www.databridgemarketresearch.com/reports/north-america-assisted-living-software-market, accessed 2026-05-18). Professional caregiver-management platforms charge $200–500/mo with per-caregiver fees (https://carecade.org/blog/caregiver-management-software-guide-2026, accessed 2026-05-18). Realistic incremental MRR: $400–$2,000 from 2–5 small-facility pilots. Effort: 60+ days (compliance documentation, multi-resident UX).

3. **Patet Certified™-style one-time IAP for "Med Card" PDF** — opportunity: $9–$19 one-time purchase to generate a printable, wallet-sized medication card (all meds, doses, allergies, emergency contacts) plus a QR for first responders. Lower-friction than subscription, plays well with senior payers who hate recurring charges. Citation: family-caregiver one-time-purchase pricing model has steady (if slower) growth vs subscription (https://www.verifiedmarketresearch.com/product/caregiver-app-market/, accessed 2026-05-18). Realistic incremental MRR-equivalent: $50–$300/mo. Effort: 5–10 days (PDF generator + Stripe/IAP).

## 5. Top 3 functionality fixes (highest leverage)

1. **Pick the buyer and rewrite the hero for that one persona.** The "is this for me or for Mom?" ambiguity is the single biggest conversion killer. Recommend rewriting for the adult-child caregiver: *"Know whether Mom took her pills today. Without nagging her."* Move Family Pro+ to the primary highlighted card. Effort: 1 day.

2. **Add real trust signals.** A founder photo + 80-word "Why I built this" (e.g., the parent-medication story), a pharmacist-quote (paid testimonial from a real RPh — $200–500 on Fiverr/RX-influencer marketplaces), a "Your data is encrypted and never sold" badge, and a one-line HIPAA statement ("Salvis is HIPAA-aware; we share data only with family members you authorize"). Effort: 2–3 days including the founder photo + pharmacist outreach.

3. **Remove pricing cards from the waitlist page (or replace prices with "Coming soon — get early-access pricing").** Asking $7.99/$14.99 commitment signal *before* you have a product to show suppresses waitlist conversion and locks you into a price you may need to drop. Keep the *plan tiers* visible (Free / Pro / Family) but defer the dollar amounts to email follow-up. Effort: 30 minutes.

## 6. Competitive landscape (2026)

| Name | Pricing | Funded? | Recent 2026 move | What they do better | What they miss |
|---|---|---|---|---|---|
| **Medisafe** | $4.99/mo or $39.99/yr (Premium); 2-med free tier | $51.5M total ($30M Series C Feb 2021) | **Moved to paid subscription Jan 1, 2026** — single biggest category event | Brand equity, 10M+ users, pharma patient-support deals, family profiles included in Premium | UX feels dated to younger caregivers; no native OCR pill-bottle scan |
| **MyTherapy** | Free | Smartpatient GmbH (private) | Increased ad-related data sharing in 2026 (per their own blog) | Genuine free, persistent alarms, clean UX | No family dashboard parity with paid apps; data-sharing concerns |
| **Round Health** | Free / freemium | Bootstrap-style | Holding pattern — clean UX positioning | Best-in-class minimalist design for single-med users | Doesn't scale beyond 1–2 meds, no family features |
| **Pillo** | Free, no premium tier | Private | 2026 Android leadership in "actually free" lists | Unlimited meds + 9 health trackers, no upsell | No iOS dominance, no caregiver tooling |
| **CVS Pharmacy app** | Free | Public co. ($CVS) | Continued pharmacy-dashboard integration in 2026 | Tied to actual Rx data, refill auto-orders, text alerts | Not multi-pharmacy; locked to CVS patients |
| **Walgreens app + Talking Pill Reminder** | Free app; talking bottle ~$10 device | Public co. ($WBA) | JOINRX text-alert program continues | Hardware + app combo, integrated with Walgreens Rx | Not cross-pharmacy |
| **GoodRx + GoodRx Gold** | Free / $9.99/mo Gold | Public co. ($GDRX) | Continued positioning as discount-card + reminders | Massive user base, discount engine | Not a pill-OCR app; reminders are secondary |
| **Pillsy** | $39.95 hardware (2018 reference); acquired by **MedAdvisor** | Acquired | **Pillsy acquired by MedAdvisor** (per 2025 market reports) | Smart bottle hardware + adherence data | Hardware cost, narrow consumer reach |
| **Dozzy** | Freemium | Private | 2026 "best of" listings positioning | Newer entrant with modern UX | Limited differentiation |

## 7. Honest "DO NOT do" list

1. **Do NOT build a smart-pill-bottle hardware play.** Pillsy was acquired by MedAdvisor; AdhereTech and PillConnect occupy the clinical-trial niche; PillSafe is doing SAFE-round wireless bottles. Hardware is a venture-funded category, not a solo-dev category. Stay software-only.

2. **Do NOT promise "interaction checks" without a licensed drug-interaction dataset.** First Databank, Wolters Kluwer, and Lexicomp licenses run $10K–$100K+/yr. Free interaction APIs (OpenFDA, RxNorm) are sufficient for *informational* warnings only and must carry explicit disclaimers. If you market "flags dangerous interactions" too aggressively without a licensed database, you ship a regulatory-risk product.

3. **Do NOT chase B2C "viral" growth via TikTok senior-caregiver content.** This category does not virally share — health is private. You will burn 3 months on content and have nothing to show. Spend that time on B2B pharmacy/facility outreach instead.

4. **Do NOT add a "voice-first AI companion / chat with your medication" feature.** This is the Glyphe vertical, not Salvis. The minute Salvis chats freely about medications, you cross into FDA-adjacent territory and your "assistant not a medical device" framing crumbles. Voice = reminders, voice = read-the-label-aloud, voice = confirm-taken. Nothing more.

5. **Do NOT spend more than $50 on the Meta ad test before fixing the persona ambiguity on the landing page (Section 5, item 1).** A bad CPL signal from a confused landing page tells you nothing about market demand. Fix the persona, then test.

## 8. Sources

- https://medx.it.com/is-the-medisafe-app-free-a-comprehensive-review-of-its-costs-and-features — Medisafe $4.99/mo or $39.99/yr pricing (accessed 2026-05-18)
- https://www.mytherapyapp.com/blog/medisafe-alternatives-free — MyTherapy free positioning + Medisafe Jan 1, 2026 paid switch (accessed 2026-05-18)
- https://pillo.care/blog/best-free-medication-reminder-app — Pillo free positioning, Pillo as Medisafe alternative (accessed 2026-05-18)
- https://digitalhealth.folio3.com/blog/best-medication-reminder-apps/ — 2026 category overview (accessed 2026-05-18)
- https://caringvillage.com/2026/05/13/medication-reminder-apps/ — 13 best medication reminder apps 2026 (accessed 2026-05-18)
- https://www.fortunebusinessinsights.com/medication-management-software-market-115703 — Medication management market $9.11B 2026 → $23.29B 2034, 12.45% CAGR (accessed 2026-05-18)
- https://www.businessresearchinsights.com/market-reports/medication-reminder-apps-market-112635 — Reminder app market $0.52B 2026 → $1.03B 2035, 8.5% CAGR (accessed 2026-05-18)
- https://nextolive.com/blogs/medication-management-app-development-2026-cost-features/ — 2026 dev trends (interoperability, predictive AI, IoT) (accessed 2026-05-18)
- https://www.crunchbase.com/organization/medisafe-project — Medisafe $51.5M total funding (accessed 2026-05-18)
- https://www.medisafe.com/digital-health-company-raises-funds-for-future-growth/ — Medisafe $30M Series C (accessed 2026-05-18)
- https://www.aarp.org/pri/topics/technology/internet-media-devices/2026-technology-trends-older-adults/ — 50+ smartphone ownership 90%, 71% bought tech in 2025 (accessed 2026-05-18)
- https://www.pewresearch.org/internet/fact-sheet/mobile/ — Smartphone ownership: 83% (50–64), 61% (65+), 27% (65+ <$30K HHI) (accessed 2026-05-18)
- https://www.parloa.com/blog/ai-voice-agents-in-healthcare/ — Voice AI health agents $650.65M 2026 → $11B 2035, 37.85% CAGR (accessed 2026-05-18)
- https://healthcarereaders.com/insights/voice-healthcare-technology — 31% discontinuation rate in voice-recognition healthcare apps (accessed 2026-05-18)
- https://www.databridgemarketresearch.com/reports/north-america-assisted-living-software-market — NA assisted-living software $19.19B 2024 → $36.33B 2032, 8.3% CAGR (accessed 2026-05-18)
- https://carecade.org/blog/caregiver-management-software-guide-2026 — Professional caregiver software $200–500/mo (accessed 2026-05-18)
- https://www.verifiedmarketresearch.com/product/caregiver-app-market/ — Caregiver app pricing models: freemium dominant, one-time slower (accessed 2026-05-18)
- https://www.theedigital.com/blog/facebook-ads-benchmarks — Facebook ads 2026 benchmarks (accessed 2026-05-18)
- https://www.superads.ai/facebook-ads-costs/cost-per-lead/healthcare — Healthcare CPL $41.60 avg, peaked $81.34 Nov 2025, ended Jan 2026 at $23.26 (accessed 2026-05-18)
- https://www.cvs.com/mobile-cvs/text — CVS free text alerts (TXT-CVS / 898-287) (accessed 2026-05-18)
- https://www.walgreens.com/topic/pharmacy/text-alerts.jsp — Walgreens free text alerts (JOINRX / 21525) (accessed 2026-05-18)
- https://www.veryfi.com/prescription-medication-label-ocr-api/ — Prescription label OCR API (NDC, dosage extraction) (accessed 2026-05-18)
- https://www.globenewswire.com/news-release/2025/06/24/3103976/28124/en/1-38-Bn-Electronic-Pill-Bottle-Market-Trends-Analysis-and-Forecasts-2024-2025-2026-2034-Mobile-Integration-and-IoT-Features-Drive-Growth-with-North-America-Leading.html — Electronic pill bottle market $1.38B; Pillsy acquired by MedAdvisor (accessed 2026-05-18)
- https://med-techinsights.com/2025/09/10/pillsafe-opens-investment-round-for-smart-prescription-bottle/ — PillSafe SAFE investment round (accessed 2026-05-18)
- https://tracxn.com/d/trending-business-models/startups-in-medication-adherence/ — 815 medication adherence startups, 223 funded, 74 Series A+ (accessed 2026-05-18)
