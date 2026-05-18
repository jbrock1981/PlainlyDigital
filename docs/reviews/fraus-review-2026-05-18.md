# Fraus — App review
**Date:** 2026-05-18
**Reviewer:** general-purpose agent (autonomous)
**Repo:** /home/jbroc/repos/Scamly (local dir; product is Fraus)

## Verdict & 12-month MRR projection

**Depends-on-CPL, realistic ceiling low.** Category has been gutted in 2026 by $0 carriers (T-Mobile, iOS 26 Call Screening, Pixel/S26 Gemini Nano) and $0 AI tools (Norton Genie, Bitdefender Scamio, Trend Micro ScamCheck). Greenlight Phase 2 only if CPL < $3 AND a differentiator beyond "Claude in a wrapper" emerges. Otherwise shelve and redirect effort to Winlet/Patet.

| Scenario | MRR (mo 12) | Key assumptions |
|---|---|---|
| Conservative | $0–$150 | CPL $6–10; build anyway; 30 paying at $4.99 blended; churn 8%/mo |
| Realistic | $300–$800 | CPL $3–5; 120–200 paying; 60/40 Individual/Family; 6%/mo churn; organic-only |
| Upside | $2.5k–$5k | Viral TikTok + AARP/state-AG editorial; 600+ paying; needs $20k+ ad spend |

Upside assumes the $40–90k portfolio ad budget — not solo-dev $50.

## 1. What it actually is (verified from code/repo)

**Landing page only, not yet deployed.** Verified:

- Next.js 14.2.35 App Router. Single route `app/page.tsx`: hero, 3-step explainer, 3 pricing cards, footer.
- `components/WaitlistForm.tsx` POSTs `{email, pricing_interest, source}` to `/api/waitlist`.
- `app/api/waitlist/route.ts` validates email regex, auto-creates `waitlist` table in Neon, upserts, captures UA + IP.
- `components/MetaPixel.tsx` fires PageView + Lead-on-success (only if `NEXT_PUBLIC_META_PIXEL_ID` set).
- TODO.md confirms no domain, no pixel ID, no DB, no USPTO filing, no Vercel deploy.

Zero of Phase 2 (Express, JWT, Claude API, Expo, RevenueCat) exists. No scam-detection code anywhere — the product is a promise.

## 2. Functionality critique
**Grade: C+**

- **Pixel correctness:** `Lead` fires only on 200 from `/api/waitlist`. `noscript` fallback present. Good.
- **Pixel gap (big):** No Conversions API. Browser-only pixel loses 30–60% of iOS conversions in 2026; Meta's bid optimizer goes blind. Add server-side CAPI.
- **No event dedup:** Same user from two pricing cards = 2 Leads. Add `eventID` UUID, pass to both pixel + CAPI.
- **Trust signals — absent (worst defect).** Zero testimonials, no founder name/photo, no FTC stat, no "we never see bank passwords" disclaimer, no sample verdicts. A 72-year-old has no reason to pick this over Norton/McAfee.
- **Social-proof footgun:** `page.tsx:24` literally renders `"Join 0+ people getting early access"`. Hide until >50.
- **Three forms on one page:** Each pricing card embeds the form. Noisy. One hero form with interest selector.
- **Hero generic:** "Catch scams before they catch you" speaks to nobody. Adult-child buyer: "Stop worrying about Mom getting scammed."
- **SEO:** Missing `twitter:card`, JSON-LD, canonical URL. Fix before paid traffic.

## 3. Sellability critique — CORE QUESTION
**Grade: D**

**Target user:** TODO.md says "adult-child-pays family model" but the landing page targets nobody. Hero speaks to the senior; Family card speaks to the adult child. A page that tries to convert both converts neither. Pick the buyer (adult child, 35–55, parent 65+) and rewrite to them.

**Alternatives today (2026, see competitive table in §6 for sources):** T-Mobile Scam Shield $0; Verizon Call Filter $0; AT&T ActiveArmor $0 basic / $7 premium (raised from $3.99 on 2026-02-18); iOS 26 Call Screening $0; Pixel + Galaxy S26 on-device Gemini Nano $0; Norton Genie $0 (in ChatGPT since 2026-03-04); Bitdefender Scamio $0; Trend Micro ScamCheck $0; McAfee bundled in $39.99/yr Essential; Truecaller Premium ~$4/mo (4M subs March 2026).

**Why switch to Fraus at $4.99–9.99: unclear.** Verdicts are commoditized at $0. Only defensible wedge is **family-tier multi-seat alerting** — but Life360 owns the family graph.

**Pricing fit:** $9.99 Family vs. $0 carrier + $0 Norton Genie is structurally hard. $4.99 Individual is DOA — Truecaller Premium is the same price with a 4M-user moat.

**Value prop rewrite:** "We text your adult kids the second a scammer targets Mom — and tell her what to do in plain English." Lead with the alert.

**First 100 paying customers come from where:** Meta CPL at 55+ runs $27–42 in 2026; at $9.99 with 10–15% senior churn, payback > LTV. Only viable: state-AG/AARP press, caregiver Facebook groups, one viral TikTok. None predictable.

**Adult-child-buys-for-parent friction: severe.** Parent must install, permission, forward. Senior new-app install completion ~25% even with adult-child setup. Free alternatives kill urgency.

**Organic/viral: none.** No public scam feed, no referral, no SEO blog. Norton Genie meanwhile got free distribution to 100M+ ChatGPT users.

## 4. Top 3 monetization opportunities

### A. Pivot Family tier to "Mom-and-Dad concierge" at $19.99/mo
Compete on **response** when a parent IS scammed: Claude-plus-human helps freeze accounts, file FTC report, call bank on three-way. FTC: elder-fraud $2.4B reported in 2024 (+26.3% YoY); true cost $10.1–81.5B ([FTC 2025-12-01](https://www.ftc.gov/system/files/ftc_gov/pdf/P144400-OlderAdultsReportDec2025.pdf)). Service biz with software assist, not $4.99 SaaS. **MRR mo 12:** $1.5–3k (75–150 customers). **Effort:** 20–30 days + part-time SLA tier.

### B. B2B2C — white-label verdict engine to senior-living + RIAs
RIAs and senior-living face FTC/state-AG duty-of-care pressure. Fraud-detection market $67.12B in 2026, 17.5% CAGR ([Fortune Business Insights 2026](https://www.fortunebusinessinsights.com/industry-reports/fraud-detection-and-prevention-market-100231)). API at $99–499/mo per facility, white-labeled. Bypasses consumer CAC. **MRR mo 12:** $500–2k (5–20 facilities). **Effort:** 15 days build, 60+ days sales.

### C. Free product + ID-theft affiliate revenue
Detection is going to $0. Free Fraus + affiliate referrals to LifeLock/Aura ($12/mo)/credit-freeze. Payout $30–80/signup. McAfee bundling at $39.99/yr proves consumers buy ID bundles around a scam moment ([McAfee 2026](https://www.mcafee.com/blogs/mcafee-news/introducing-mcafees-scam-detector-now-included-in-all-core-plans/)). **MRR mo 12:** $500–1.5k if free-tier hits 10k MAU. **Effort:** 10 days.

### $50 ad-budget honesty check
At 2026 senior-vertical CPL $27–42, $50 yields 1–2 leads — statistically meaningless. Portfolio plan budgets $40–90k for scale; that's the real PMF number, and carriers cap the ceiling even then. Reframe the $50 test as headline/audience click validation, not buy/build economics. Build/no-build hinges on differentiator clarity.

## 5. Top 3 functionality fixes

**A. Add Meta CAPI server-side from `/api/waitlist/route.ts`** — server-side `Lead` with hashed email + eventID dedup. Browser-only pixel loses 30–60% iOS conversions in 2026 and starves Meta's optimizer (inflates CPL 25–40%). 0.5 day.

**B. Rewrite landing to adult-child buyer + heavy trust signals** — single hero CTA ("Protect Mom and Dad from scammers"), founder name+photo, 5 caregiver testimonials, FTC stat callout, sample verdict screenshot, "we never see bank passwords" disclaimer, FAQ. Kill the three duplicate forms. Current page has no buyer and no trust. 2–3 days.

**C. Public "scams caught this week" feed** — `/scams` page publishing anonymized flagged scams with plain-English explainers, weekly, free, no signup. Closes the zero-SEO gap; scam content is highly searchable. 4–5 days.

## 6. Competitive landscape (2026)

| Name | Pricing | 2026 move | Better at | Misses |
|---|---|---|---|---|
| T-Mobile Scam Shield | $0 / $4 prem | AI updates every 6 min | Network call blocking, 100M+ reach | Text/email/voicemail |
| Verizon Call Filter | $0 / $2.99 prem | Forwards risk-calls to vm | Default-on Verizon base | Call-only |
| AT&T ActiveArmor | $0 / $7 (raised 2026-02-18) | Added $1M ID-fraud reimb | Bundles calls + ID + VPN | Not family-graph |
| iOS 26 Call Screening | $0 | Shipped 2026 with iOS 26 | On every iPhone | Just transcribes; no verdict |
| Pixel + Galaxy S26 | $0 | Gemini Nano on-device; expanding to WhatsApp/IG/Signal | On-device AI privacy | Pixel/S26 only |
| Norton Genie | $0 | In ChatGPT 2026-03-04 | Free + 100M ChatGPT distribution | No family-graph/alerting |
| Bitdefender Scamio | $0 | WhatsApp/Messenger/Discord chatbot | Zero-friction install | No subscription |
| Trend Micro ScamCheck | $0 | Free browser + mobile | Cross-platform free | Brand vs Norton |
| McAfee Scam Detector | $39.99/yr bundle | Bundled into core 2026 | Inline scan iMessage/WhatsApp on Android | iPhone is filtered folder only |
| Truecaller Premium | ~$4/mo | 4M subs March 2026 (+70% iOS YoY) | Caller-ID DB moat | India/MEA-skewed |
| Carefull | $9.99/mo | $16.5M Series A | Bank-account behavior monitoring | Not scam-content |
| EverSafe | ~$8–25/mo | Account aggregation | Bank-level + family circle | Not LLM verdict |

**Are there ANY profitable consumer scam-detection apps?**

Honest read: the pure scam-text/email-verdict layer is commoditizing to $0 in 2026. Profitable adjacents:

- **Truecaller** — profitable on a caller-ID database moat (US can't be replicated).
- **Carefull / EverSafe** — profitable on **bank-account read access**, not scam verdicts.
- **Aura / LifeLock** — profitable on identity-theft insurance, not detection.
- **Carrier premium tiers** — profitable by definition (incremental ARPU, zero CAC).

The solo-dev wedge is NOT detection. It's **family-graph + real-time response service.** Pure detection at $4.99–9.99/mo against $0 carrier + $0 Norton + $0 Bitdefender + $0 iOS 26 is structurally unprofitable.

## 7. Honest "DO NOT do" list

1. **Do not build Expo mobile yet.** App Store + Play Store submission is 2–4 weeks of overhead with no PMF signal. Web PWA first, validate paying conversion, then go native.
2. **Do not file USPTO intent-to-use ($350) yet.** File after $300 MRR or 2,500 waitlist signups, whichever first.
3. **Do not build voice/voicemail analysis in v1.** Whisper/Deepgram add cost and latency for a feature 80% of users won't touch; FTC 2025 data shows senior-targeting scams are SMS + email dominant.
4. **Do not build phone-call blocking.** TODO.md correctly excludes it. Carriers own this with network-level data Fraus cannot get.
5. **Do not run $40k+ Meta spend before a differentiator exists.** Spending it on current positioning is paying Meta to compete with Norton Genie's free product. Differentiate first (family-graph service tier), spend second.

## 8. Sources

- [FTC — Social Media Scams (2026-04)](https://www.ftc.gov/news-events/news/press-releases/2026/04/new-ftc-data-show-people-have-lost-billions-social-media-scams)
- [FTC — Protecting Older Consumers 2024–2025 (2025-12-01)](https://www.ftc.gov/system/files/ftc_gov/pdf/P144400-OlderAdultsReportDec2025.pdf)
- [Trend Micro ScamCheck (2026)](https://www.trendmicro.com/en_us/forHome/products/trend-micro-scam-check.html)
- [Gen Digital — Norton Genie in ChatGPT (2026-03-04)](https://newsroom.gendigital.com/2026-03-04-The-Worlds-First-AI-Powered-Scam-Detector,-Norton-Genie,-Now-in-ChatGPT)
- [TechCrunch — $2.1B social-media scams 2025 (2026-04-27)](https://techcrunch.com/2026/04/27/consumers-lost-2-1-billion-to-social-media-scams-in-2025-tc-reports/)
- [PYMNTS — Fraud Losses Quintupled Since 2020 (2026)](https://www.pymnts.com/fraud-prevention/2026/consumer-fraud-losses-quintupled-since-2020-ftc-says/)
- [T-Mobile Scam Shield (2026)](https://www.t-mobile.com/benefits/scam-shield)
- [Sotros — Facebook Ads CPL 2026](https://sotrosinfotech.com/blog/average-cost-per-lead-facebook-ads-benchmarks/)
- [CNBC — $81.5B elder fraud 2024 (2025-12-13)](https://www.cnbc.com/2025/12/13/financial-fraud-seniors-ftc.html)
- [Truecaller — 4M premium subs (March 2026)](https://www.prnewswire.com/news-releases/truecaller-surpasses-4-million-premium-subscribers-302709354.html)
- [Macworld — iOS 26 Call Screening (2026)](https://www.macworld.com/article/2935514/my-favorite-ios-26-feature-has-banished-spam-callers-once-and-for-all.html)
- [9to5Google — Scam Detection on S26 (2026-02-25)](https://9to5google.com/2026/02/25/google-messages-scam-detection-gemini/)
- [AT&T ActiveArmor pricing (2026-02-18)](https://www.att.com/support/article/wireless/000116671/)
- [Bitdefender Scamio (2026)](https://www.bitdefender.com/en-us/consumer/scamio)
- [McAfee Scam Detector in core plans (2026)](https://www.mcafee.com/blogs/mcafee-news/introducing-mcafees-scam-detector-now-included-in-all-core-plans/)
- [Fortune Business Insights — Fraud Detection Market 2026](https://www.fortunebusinessinsights.com/industry-reports/fraud-detection-and-prevention-market-100231)
