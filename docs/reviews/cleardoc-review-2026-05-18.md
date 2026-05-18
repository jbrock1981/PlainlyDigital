# ClearDoc — App review
**Date:** 2026-05-18
**Reviewer:** general-purpose agent (autonomous)
**Repo:** /home/jbroc/repos/ClearDoc

## Verdict & 12-month MRR projection

**Shelve unless the medical-bills pivot ships with a free tier, an annual SKU, and dispute-letter export. Free ChatGPT photo-of-bill eats the generic category; only a narrow medical-bills lane has defensible pull.**

| Scenario | MRR (month 12) | Key assumptions |
|---|---|---|
| Conservative | $80–$200 | Ship as-is, no pivot. ~30 subs, 10-12% monthly churn, $50 ad budget. |
| Realistic | $300–$700 | Rename, drop to $4.99/mo + $29.99/yr, ship history + CPT lookup + dispute-letter export. ~80-130 subs, 8-10% churn. |
| Upside | $1,200–$2,500 | Above + a viral TikTok + Goodbill-adjacent SEO. Still capped by free-ChatGPT ceiling. |

## 1. What it actually is (verified from code/repo)

- **Camera-first Expo SDK 54 app** posting base64 to a Firebase Cloud Function (`functions/src/analyzeDocument.ts:41`) calling `claude-sonnet-4-20250514`.
- **Generic schema** (`document_type`, `plain_summary`, `action_items[]`, `money{...}`, `red_flags[]`, `confidence` — `parse-result.ts:22`). One prompt, no per-doc-type templates.
- **Pricing diverged from the brief's premise.** Not "$7.99 monthly-only" — code ships 1 free scan, `cleardoc_pack20` $4.99, `cleardoc_monthly` $7.99/mo (`config.ts:12,25-39`). No annual.
- **Server guardrails are real** — daily kill-switch, transactional quota gate, hashed-uid audit, SSN/card regex redact on top of prompt redaction.
- **Anonymous auth only in v1**, Apple/Google deferred (`ROADMAP.md:21-22`). Uninstall = orphaned history + entitlement. Should be a launch-blocker.

## 2. Functionality critique
**Grade: B-**

- **Works end-to-end:** capture → typed JSON with Zod + redaction (`parse-result.ts:99-105`); race-safe quota gate in `recordScan` transaction (`analyzeDocument.ts:60-65,113`) with `quota-race.test.ts`; RevenueCat paywall with restore (`paywall.tsx:65-73`).
- **Broken or unfinished:**
  - **No medical-bill history UI.** `history.tsx` is generic — no provider/claim/date filtering. Medical bills cluster over 30-90 days per episode.
  - **No CPT/HCPCS lookup.** Plan calls for it; no dataset, no `lib/cpt-lookup.ts`, no UI.
  - **No dispute-letter PDF export.** Result only shares `plain_summary` via OS share (`result.tsx:54-56`). The artifact is what IQBill/CareRoute/Resolve sell on.
  - **No annual SKU.** Roadmap defers. Avg mobile sub churn ~9%/mo (RevenueCat 2026); annual collapses renewal decisions to once/year.
- **Where users get stuck:** anonymous-auth uninstall destroys history; 1-scan trial dies on the first blurry photo; no confidence-low retry despite `ROADMAP.md:35`.
- **AI extraction quality:** generic prompt collapses a 20-line hospital bill into one `money.breakdown` string. EOB allowed-vs-responsibility math not modeled. CPT codes not structured. No golden-output tests. Adequate for "what does this say"; inadequate as a medical-billing tool.
- **Test coverage:** ~85 client / ~49 function test cases (grep). Schema, quota race, RC webhook, redaction covered. Missing: Anthropic golden fixtures, e2e (despite `playwright.config.ts`), Firestore rules (despite `firestore-rules-tests/`). Solid unit, thin integration.

## 3. Sellability critique
**Grade: D**

**Target user (specific):** Officially "anyone confused by a document." Honestly **yes, too generic to acquire** — $4-8 CPI on Meta/TikTok with no organic search intent. Medical-bills pivot is the right narrowing; EOB-only is sharper but probably too small for App Store discovery.

**Their alternative today (name + price):**
- **Free ChatGPT/Claude/Gemini photo upload** — $0. Fox News 2026 documented the workflow that took a $195K bill down 83%.
- **Bill Shield** (Google Play, updated 2026-02-07) — freemium AI bill scan.
- **Medical Bill Reader** (medicalbillreader.com) — free plain-English upload.
- **Goodbill** — 0% upfront, 20% of savings, cap $1,000 — risk-free framing.
- **IQBill / Reclaim / CareRoute / Resolve** — IQBill sells specifically on ready-to-send appeal letters.

**Reason they'd switch:**
- **Pricing fit:** $7.99/mo is mispriced for sporadic medical-bill use. Avg mobile sub churn ~9% monthly (RevenueCat 2026). ClearDoc has no habit loop. Pull to $4.99/mo + $29.99/yr.
- **Value prop today:** "Snap a photo of any confusing document, get plain English." That is exactly what free ChatGPT does. **Why pay?**
- **First 100:** friends/family + $50 Meta test. No SEO, no viral hook.
- **First 1000:** requires the rename + a TikTok content engine ("found a $1,300 error on my hospital bill") + sharable artifact (dispute-letter PDF).
- **Organic / viral mechanics:** none. No share-result deep link, no family-share surface. Paywall sells "save scans," not "send my partner the explanation."

## 4. Top 3 monetization opportunities

1. **Pivot to a medical-bills brand, $4.99/mo + $29.99/yr, generous free tier.** Citation: 40% of adults with employer coverage report difficulty understanding what their health plan covers; 44% difficulty understanding out-of-pocket cost — KFF/LA Times Survey (https://www.kff.org/private-insurance/kaiser-family-foundation-la-times-survey-of-adults-with-employer-sponsored-insurance/). +$200-500 MRR at month 6. Effort: 10-14 days.

2. **Dispute-letter / appeal-letter PDF export, Pro-gated.** Citation: Fox News 2026 "AI helps man reduce $195K hospital bill by 83%" (https://www.foxnews.com/tech/163k-fake-medical-bill-charges-ai-uncovers-you); IQBill positions explicitly on personalized letters + phone scripts (https://apps.apple.com/us/app/medical-bill-negotiator-iq/id6757212060, live 2026). +$150-400 MRR. Effort: 5-7 days.

3. **Goodbill-style affiliate handoff on bills above a threshold.** Citation: Goodbill — 20% of savings, cap $1,000, $0 if no reduction (https://help.goodbill.com/en/articles/254209, 2026). Surface "want help negotiating?" → affiliate URL. Mirrors Patet's affiliate pattern. +$50-300 MRR. Effort: 2-3 days.

**On the rename+pivot:** medical bills > EOB-only > legal docs / contracts / gov forms. Legal docs carry liability ("is this legal advice?"); contracts are B2B-shaped; gov forms have thin seasonality and no recurring revenue hook; EOB-only is too narrow for store discovery (keep EOBs as a feature inside the medical-bills app).

## 5. Top 3 functionality fixes

1. **Apple Sign-In + Google Sign-In** (replace anonymous-only). Fix: orphan-data-on-uninstall destroys retention and trips App Store reviewer notes. Effort: 3 days. Currently on the v1.x roadmap (`ROADMAP.md:21`) — promote it to launch-blocker.

2. **Confidence-low retry UX.** Fix: 1-free-scan trial is consumed by a single blurry photo today, killing first-impression conversion. Surface "I'm not sure — scan again with more light?" inline before counting against quota. Already on roadmap (`ROADMAP.md:35`), should be Phase 1. Effort: 2 days.

3. **Bill history screen with provider + amount filtering.** Fix: medical bills come in clusters (hospital + radiology + anesthesia + lab for one ER visit) — users need to view them together. Existing `history.tsx` is a flat list. Effort: 4-5 days.

## 6. Competitive landscape (2026)

| Name | Pricing | Funded? | 2026 move | Better | Misses |
|---|---|---|---|---|---|
| **ChatGPT/Claude/Gemini photo** | $0 | Yes (massively) | ChatGPT Health + Clinicians launches; Axios 2026-01-05 insurance piece | Free, multimodal, installed, daily habit | No bill UX, no history, no letter, no camera |
| **Bill Shield** | Freemium | Small | Updated 2026-02-07 | Sharper positioning | Android-led, thin iOS/SEO |
| **IQBill** | App Store sub | Small | Live 2026: letters + scripts + plans | Ships the artifact | Low brand recognition |
| **Medical Bill Reader** (web) | Free | Bootstrap | Free CPT/ICD-10 decoding 2026 | Zero-friction free web | No app, no actions |
| **Reclaim** | Freemium | Unclear | Long-running, full bill manager | Tracks accuracy + payments | Less AI-native |
| **Goodbill** | 20% of savings, cap $1,000 | Funded | Active 2026, BBB-reviewed | Risk-free + human negotiation | Not self-serve, not $/mo |
| **Resolve Medical Bills** | Service fee | Funded | Active 2026 advocacy | Human advocate | Not a consumer app |
| **CareRoute** | Content + tools | Bootstrap | Free scripts/templates 2026 | Owns negotiation SEO | Lighter tool depth |
| **BillKarma** | Free scanner | Unclear | 60s no-account scan + per-hospital pages | Frictionless + SEO | Web-only |
| **FAIR Health Consumer** | Free | Nonprofit | Mobile + Spanish + estimator | Trusted, free | Estimator, not explainer |

**Elephant — free ChatGPT photo-of-bill** is the category killer. Fox News 2026 documented end-to-end the workflow ClearDoc charges $7.99/mo for. "Why pay?" answers: (a) one-tap camera vs. image-select, (b) saved history, (c) dispute-letter PDF, (d) family sharing. ClearDoc has (a); (b)-(d) are roadmap. **Without (c) and (d) there is no moat,** and OpenAI is actively expanding into health.

## 7. Honest "DO NOT do" list

1. **No iPad-optimized layout, AR overlay, or "Pro photo" features.** Win is structured output (letter, lookup, history), not capture quality.
2. **No B2B "API for clinics" pivot.** Solo-dev scope, two-year sales cycles.
3. **No chatbot ("ask follow-up questions about your bill").** That is literally ChatGPT — lose that fight by design.
4. **No Spanish localization before $500 MRR.** Linear cost; ship after a paying base exists.
5. **No $59.99–$69.99 annual SKU (roadmap placeholder).** Medical bills are sporadic — $24.99–$29.99/yr is the right shape.

## 8. Sources

- KFF / LA Times Survey of Adults with Employer-Sponsored Insurance — https://www.kff.org/private-insurance/kaiser-family-foundation-la-times-survey-of-adults-with-employer-sponsored-insurance/ (2026)
- Fox News "AI helps man reduce $195K hospital bill by 83%" — https://www.foxnews.com/tech/163k-fake-medical-bill-charges-ai-uncovers-you (2026)
- Axios "ChatGPT helps users navigate health care and health insurance" — https://www.axios.com/2026/01/05/chatgpt-openai-health-insurance-aca (2026-01-05)
- Medical Economics "OpenAI launches ChatGPT Health" — https://www.medicaleconomics.com/view/openai-launches-chatgpt-health-directly-linking-patient-portals-to-the-ai-chatbot (2026)
- Fierce Healthcare "ChatGPT for Clinicians" — https://www.fiercehealthcare.com/ai-and-machine-learning/openai-launches-chatgpt-clinicians-free-ai-tool-physicians-nps-and (2026)
- Goodbill help center — https://help.goodbill.com/en/articles/254209 (2026)
- Goodbill patient page — https://www.goodbill.com/patients (2026)
- IQBill — https://apps.apple.com/us/app/medical-bill-negotiator-iq/id6757212060 (2026)
- Bill Shield (updated 2026-02-07) — https://play.google.com/store/apps/details?id=com.billshield.app
- Medical Bill Reader — https://medicalbillreader.com/ (2026)
- Reclaim — https://apps.apple.com/us/app/reclaim-manage-medical-bills/id1361302053 (2026)
- BillKarma — https://billkarma.app/guides/understanding-explanation-of-benefits/ (2026)
- CareRoute — https://www.careroute.ai/blog/lowering-medical-bills (2026)
- Resolve Medical Bills — https://www.resolvemedicalbills.com/ (2026)
- FAIR Health Consumer — https://www.fairhealthconsumer.org/ (2026)
- CNBC Select "best bill negotiation services of 2026" — https://www.cnbc.com/select/best-bill-negotiation-services/ (2026)
- Slate "I Saved $800 on My Medical Bills" — https://slate.com/technology/2026/04/hospital-bill-insurance-negotiation-how-to.html (2026-04)
- Managed Healthcare Executive (1-in-5 surprise-bill stat) — https://www.managedhealthcareexecutive.com/view/healthcare-price-transparency-reality-or-mirage (2026)
- CMS Hospital Price Transparency, CY2026 OPPS, enforcement 2026-04-01 — https://www.cms.gov/priorities/key-initiatives/hospital-price-transparency
- RevenueCat 2026 utility benchmarks — https://www.revenuecat.com/state-of-subscription-apps-2026-utilities/ (~9% monthly avg)
- Adapty utilities benchmarks 2026 — https://adapty.io/blog/utilities-app-subscription-benchmarks/
- Go Medical Billing CPT lookup (2026) — https://www.gomedicalbilling.com/tools/cpt-lookup
- Internal: /home/jbroc/.claude/plans/swift-wobbling-crystal.md (2026-05-09)
- Internal: /home/jbroc/repos/ClearDoc/ — CLAUDE.md, STATUS.md, ROADMAP.md, src/app/{index,paywall,result}.tsx, src/constants/config.ts, functions/src/{analyzeDocument.ts, lib/anthropic.ts, lib/parse-result.ts}
