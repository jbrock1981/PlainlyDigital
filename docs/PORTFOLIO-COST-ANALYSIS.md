# Plainly Digital LLC — Portfolio Cost vs. Profit Analysis
**Prepared: March 30, 2026 | Standardized Pricing Model**

---

## Pricing Standard (All 4 Apps)

Based on Winlet's proven model, all apps standardize on:

| Tier | Monthly | Annual | AI Calls/Day | AI Calls/Month | Chat Model |
|------|---------|--------|-------------|---------------|------------|
| **Free** | $0 | — | 5-10 | 30-60 | Haiku 4.5 |
| **Pro** | $5.99 | $49.99 | 40 | 500 | Haiku 4.5 |
| **Pro Max** | $9.99 | $79.99 | 80 | 1,200 | Sonnet 4.6 (100/mo cap, then Haiku) |

**Boost Packs (all apps):** $1.99 → +50 calls | $4.99 → +200 calls

---

## API Cost Basis

| Model | Input (per MTok) | Output (per MTok) | Notes |
|-------|-----------------|-------------------|-------|
| Claude Sonnet 4.6 | $3.00 | $15.00 | Coach chat, complex analysis |
| Claude Haiku 4.5 | $0.80 | $4.00 | Nudges, feed, structured extraction |

**Per-call cost estimates:**

| Call Type | Avg Input Tokens | Avg Output Tokens | Cost/Call |
|-----------|-----------------|-------------------|-----------|
| Haiku chat (simple) | 750 | 256 | $0.002 |
| Haiku structured (feed/nudge) | 500 | 150 | $0.001 |
| Haiku vision (food photo) | 1,500 | 512 | $0.003 |
| Sonnet chat (coaching) | 2,500 | 512 | $0.015 |
| Sonnet chat (long context) | 3,500 | 1,024 | $0.026 |
| Sonnet analysis (insights) | 2,000 | 500 | $0.014 |
| Sonnet generation (resume/review) | 3,000 | 600 | $0.018 |

---

## Fixed Monthly Costs (Per App)

| Item | Cost/Month | Notes |
|------|-----------|-------|
| Database (Neon/Supabase Pro) | $25 | Serverless PostgreSQL |
| Hosting (Vercel/Render Pro) | $20 | API + static hosting |
| Domain + SSL | $3 | Annual amortized |
| Error monitoring (Sentry) | $26 | Developer plan |
| Analytics (PostHog) | $0 | Free tier |
| **Total fixed per app** | **$74** | |
| **Total fixed (4 apps)** | **$296** | |

---

## Revenue Deductions

| Deduction | Year 1 | Year 2+ |
|-----------|--------|---------|
| Apple/Google fee | 30% | 15% (Small Business Program, <$1M) |
| Net per $5.99/mo (Pro) | $4.19 | $5.09 |
| Net per $9.99/mo (Pro Max) | $6.99 | $8.49 |
| Net per $49.99/yr (Pro annual) | $2.92/mo | $3.54/mo |
| Net per $79.99/yr (Pro Max annual) | $4.67/mo | $5.67/mo |
| Net per $1.99 boost | $1.39 | $1.69 |
| Net per $4.99 power boost | $3.49 | $4.24 |

---

# 1. PLAINLY — Financial Literacy App

## AI Call Sites (6 endpoints)

| Endpoint | Model | Cost/Call | Frequency (casual) | Frequency (power) |
|----------|-------|-----------|--------------------|--------------------|
| Sage Coach chat | Haiku (Free/Pro) / Sonnet (Pro Max) | $0.002 / $0.026 | 3/day | 10/day |
| Coach nudge (lesson/milestone) | Haiku | $0.001 | 1/day | 3/day |
| Weekly summary | Haiku | $0.001 | 1/week | 1/week |
| Personalized feed | Haiku | $0.002 | 1/day (cached 12h) | 1/day |
| Feed weekly card | Haiku | $0.001 | 1/week | 1/week |
| Certification grading | Haiku | $0.001 | 0/month | 1/month |

## Per-User Monthly AI Costs

| User Type | Calls/Month | Model | API Cost/Month |
|-----------|------------|-------|---------------|
| **Free casual** | ~30 (3 chats + 1 nudge + 1 feed/day × 7 days/week) | Haiku | **$0.04** |
| **Free engaged** | ~60 (maxes daily limit) | Haiku | **$0.08** |
| **Pro casual** | ~120 (5 chats + 2 nudges + 1 feed/day × 20 days) | Haiku | **$0.16** |
| **Pro engaged** | ~400 | Haiku | **$0.53** |
| **Pro Max casual** | ~120 (mix: 60 Sonnet + 60 Haiku) | Sonnet+Haiku | **$0.97** |
| **Pro Max engaged** | ~500 (100 Sonnet cap + 400 Haiku) | Sonnet+Haiku | **$2.72** |
| **Pro Max power** | ~1,200 (100 Sonnet + 1,100 Haiku) | Sonnet+Haiku | **$4.82** |

## Revenue Streams

### 1. Subscriptions (Primary)

| Tier | Monthly Net (Y1) | Casual Cost | Casual Margin | Power Cost | Power Margin |
|------|-----------------|-------------|---------------|------------|--------------|
| Free | $0 | $0.04 | -$0.04 (loss leader) | $0.08 | -$0.08 |
| Pro monthly | $4.19 | $0.16 | **$4.03 (96%)** | $0.53 | **$3.66 (87%)** |
| Pro annual | $2.92/mo | $0.16 | **$2.76 (95%)** | $0.53 | **$2.39 (82%)** |
| Pro Max monthly | $6.99 | $0.97 | **$6.02 (86%)** | $4.82 | **$2.17 (31%)** |
| Pro Max annual | $4.67/mo | $0.97 | **$3.70 (79%)** | $4.82 | **-$0.15 (-3%)** |

**Key finding:** Pro Max annual power users are break-even/slight loss. This is acceptable because:
- Very few users will max 1,200 calls/month consistently
- The 100 Sonnet cap limits the expensive model usage
- Boost pack purchases from these power users offset losses
- Annual plan locks in 12 months of revenue

### 2. Affiliate Revenue (Secondary)
- 11 curated products across 7 categories (HYSA, credit cards, investing, budgeting, credit builders, student loans, insurance)
- Typical fintech affiliate commissions:
  - HYSA referral: $50-150 per funded account
  - Credit card referral: $50-200 per approved card
  - Investment platform: $50-100 per funded account
  - Budgeting tool (YNAB): $15-30 per subscription
  - Credit builder: $25-50 per sign-up
  - Insurance: $10-25 per policy

| Metric | Conservative | Moderate | Optimistic |
|--------|-------------|----------|-----------|
| Monthly active users | 500 | 2,500 | 10,000 |
| Affiliate click rate | 2% | 4% | 6% |
| Conversion rate | 5% | 8% | 12% |
| Avg commission | $40 | $60 | $80 |
| **Monthly affiliate revenue** | **$20** | **$480** | **$5,760** |

### 3. Certification (Future)
- Financial literacy credential (shareable, publicly verifiable)
- Potential: $9.99-19.99 one-time fee for certificate issuance
- Employer/university bulk pricing for validated credentials

### 4. Boost Pack Revenue

| Scenario | Buyers/Month | Avg Pack | Net Revenue |
|----------|-------------|----------|------------|
| Conservative (2% of paid) | 5 | $1.99 | $6.95 |
| Moderate (5% of paid) | 25 | $3.49 avg | $87.25 |
| Optimistic (8% of paid) | 80 | $3.49 avg | $279.20 |

## Plainly Break-Even & Projections

**Break-even (fixed costs only):** $74 ÷ $4.19 net = **18 Pro monthly subscribers**

| Month | Free | Pro | Pro Max | Sub MRR | Affiliate | Boosts | Total MRR | Net (- fixed) |
|-------|------|-----|---------|---------|-----------|--------|-----------|---------------|
| 3 | 200 | 40 | 10 | $268 | $25 | $15 | **$308** | $234 |
| 6 | 600 | 120 | 30 | $801 | $120 | $45 | **$966** | $892 |
| 12 | 2,000 | 350 | 80 | $2,263 | $480 | $130 | **$2,873** | $2,799 |
| 18 | 5,000 | 800 | 200 | $5,354 | $1,500 | $300 | **$7,154** | $7,080 |
| 24 | 10,000 | 1,500 | 400 | $10,275 | $4,000 | $560 | **$14,835** | $14,761 |

*Assumes 60% Pro monthly / 40% annual mix. Year 2+ uses 15% store fee.*

---

# 2. WINLET — Achievement Tracking App

## AI Call Sites (9 endpoints)

| Endpoint | Model | Cost/Call | Frequency (casual) | Frequency (power) |
|----------|-------|-----------|--------------------|--------------------|
| Sage Chat | Haiku (Free/Pro) / Sonnet (Pro Max) | $0.002 / $0.026 | 2/day | 8/day |
| Pattern analysis | Sonnet | $0.014 | 1/week | 2/week |
| Reflection prompt | Sonnet | $0.008 | 1/week | 1/day |
| Weekly summary | Sonnet | $0.012 | 1/week | 1/week |
| Monthly report | Sonnet | $0.014 | 1/month | 1/month |
| Resume narrative | Sonnet | $0.006 × N categories | 0/month | 1/month (×5 cats) |
| Year in review | Sonnet | $0.018 | 0/month | 1/year |
| Conversation summarize | Sonnet | $0.012 | 0 (unused) | 0 |
| Crisis classification | Sonnet | $0.001 | 0 (Layer 2, rare) | 0 |

## Per-User Monthly AI Costs

| User Type | Calls/Month | Model | API Cost/Month |
|-----------|------------|-------|---------------|
| **Free casual** | ~20 (2 chats/day × 10 days) | Haiku | **$0.03** |
| **Free engaged** | ~30 (maxes limit) | Haiku | **$0.05** |
| **Pro casual** | ~80 (3 chats/day + weekly insights) | Haiku | **$0.18** |
| **Pro engaged** | ~300 | Haiku | **$0.62** |
| **Pro Max casual** | ~80 (50 Sonnet + 30 Haiku) | Sonnet+Haiku | **$1.36** |
| **Pro Max engaged** | ~500 (100 Sonnet + 400 Haiku) | Sonnet+Haiku | **$3.40** |
| **Pro Max power** | ~1,200 (100 Sonnet + 1,100 Haiku) | Sonnet+Haiku | **$4.82** |

## Revenue Streams

### 1. Subscriptions (Primary)

| Tier | Monthly Net (Y1) | Casual Cost | Casual Margin | Power Cost | Power Margin |
|------|-----------------|-------------|---------------|------------|--------------|
| Free | $0 | $0.03 | -$0.03 | $0.05 | -$0.05 |
| Pro monthly | $4.19 | $0.18 | **$4.01 (96%)** | $0.62 | **$3.57 (85%)** |
| Pro Max monthly | $6.99 | $1.36 | **$5.63 (81%)** | $4.82 | **$2.17 (31%)** |

### 2. Boost Packs
Same pricing structure as Plainly. Winlet already has this implemented.

### 3. Premium Exports (Future Upsell Potential)
- **Life Resume** — polished HTML export of accomplishments. Could be $4.99 one-time or included in Pro Max.
- **Year in Review** — Spotify Wrapped-style annual narrative. Premium feature for Pro Max only.
- **Proof Folder** — exportable portfolio of accomplishments for job applications.

### 4. B2B/Enterprise (Future)
- Employee wellness programs (accomplishment tracking for teams)
- White-label for HR platforms

## Winlet Break-Even & Projections

**Break-even:** $74 ÷ $4.19 = **18 Pro monthly subscribers**

| Month | Free | Pro | Pro Max | Sub MRR | Boosts | Total MRR | Net |
|-------|------|-----|---------|---------|--------|-----------|-----|
| 3 | 150 | 30 | 8 | $182 | $10 | **$192** | $118 |
| 6 | 400 | 80 | 20 | $475 | $30 | **$505** | $431 |
| 12 | 1,200 | 200 | 50 | $1,192 | $75 | **$1,267** | $1,193 |
| 18 | 3,000 | 500 | 120 | $2,936 | $180 | **$3,116** | $3,042 |
| 24 | 6,000 | 1,000 | 250 | $5,937 | $350 | **$6,287** | $6,213 |

---

# 3. VINLA — Health & Wellness App

## AI Call Sites (8 endpoints)

| Endpoint | Model | Cost/Call | Frequency (casual) | Frequency (power) |
|----------|-------|-----------|--------------------|--------------------|
| Sage Health Coach | Haiku (Free/Pro) / Sonnet (Pro Max) | $0.002 / $0.026 | 3/day | 10/day |
| Food photo vision | Haiku (vision) | $0.003 | 0/day | 3/day |
| Weekly insights | Sonnet | $0.014 | 1/week | 1/week |
| Health signals | Haiku | $0.002 | 1/day (cached) | 1/day |
| Meal plan (7-day) | Sonnet | $0.018 | 0/month | 2/month |
| Proactive nudges | Haiku | $0.001 | 1/day | 3/day |
| Wrapped narrative | Sonnet | $0.012 | 0/month | 1/year |
| Journal prompts | Haiku | $0.001 | 1/day | 1/day |

## Per-User Monthly AI Costs

| User Type | Calls/Month | Model | API Cost/Month |
|-----------|------------|-------|---------------|
| **Free casual** | ~30 (3 chats + 1 signal + 1 nudge/day × 6 days) | Haiku | **$0.04** |
| **Free engaged** | ~60 (maxes limit) | Haiku | **$0.10** |
| **Pro casual** | ~150 (5 chats + 2 photos + signals + nudge/day) | Haiku | **$0.22** |
| **Pro engaged** | ~400 (+ meal plans, insights) | Haiku | **$0.58** |
| **Pro Max casual** | ~150 (80 Sonnet + 70 Haiku) | Sonnet+Haiku | **$2.22** |
| **Pro Max engaged** | ~500 (100 Sonnet + 400 Haiku) | Sonnet+Haiku | **$3.40** |
| **Pro Max power** | ~1,200 (100 Sonnet + 1,100 Haiku) | Sonnet+Haiku | **$4.82** |

## Revenue Streams

### 1. Subscriptions (Primary)

| Tier | Monthly Net (Y1) | Casual Cost | Casual Margin | Power Cost | Power Margin |
|------|-----------------|-------------|---------------|------------|--------------|
| Free | $0 | $0.04 | -$0.04 | $0.10 | -$0.10 |
| Pro monthly | $4.19 | $0.22 | **$3.97 (95%)** | $0.58 | **$3.61 (86%)** |
| Pro Max monthly | $6.99 | $2.22 | **$4.77 (68%)** | $4.82 | **$2.17 (31%)** |
| Student annual | $2.33/mo | $0.22 | **$2.11 (91%)** | $0.58 | **$1.75 (75%)** |
| Founding annual | $2.33/mo | $0.22 | **$2.11 (91%)** | $0.58 | **$1.75 (75%)** |

### 2. Boost Packs
Same structure. Vinla's health-focused power users (meal plan generation, daily photo logging) are likely boost buyers.

### 3. Special Pricing Tiers
- **Student** ($39.99/yr = $2.33/mo net after store fee): Healthy margins even for engaged users
- **Founding Member** ($39.99/yr locked for life): First 10,000 users. Builds community loyalty. Same economics as student tier.

### 4. Future Revenue
- Wearable integrations (Apple Health, Fitbit, Garmin)
- Nutritionist referral partnerships
- Corporate wellness programs

## Vinla Break-Even & Projections

**Break-even:** $74 ÷ $4.19 = **18 Pro monthly subscribers**

| Month | Free | Pro | Pro Max | Student/Founding | Sub MRR | Boosts | Total MRR | Net |
|-------|------|-----|---------|-----------------|---------|--------|-----------|-----|
| 3 | 100 | 25 | 5 | 15 | $175 | $8 | **$183** | $109 |
| 6 | 350 | 80 | 15 | 50 | $521 | $25 | **$546** | $472 |
| 12 | 1,000 | 250 | 50 | 150 | $1,746 | $80 | **$1,826** | $1,752 |
| 18 | 3,000 | 600 | 120 | 350 | $4,126 | $200 | **$4,326** | $4,252 |
| 24 | 7,000 | 1,200 | 250 | 700 | $8,383 | $400 | **$8,783** | $8,709 |

*Includes student/founding at $2.33/mo net per subscriber.*

---

# 4. NOTCH — AI Life Advisor App

## AI Call Sites (28+ endpoints — most AI-intensive app)

| Category | Endpoints | Model | Cost/Call | Frequency (casual) | Frequency (power) |
|----------|-----------|-------|-----------|--------------------|--------------------|
| Sage Chat | 1 | Haiku/Sonnet | $0.002/$0.026 | 3/day | 10/day |
| Career tools | 3 (resume, interview, cover letter) | Sonnet | $0.018 avg | 0/week | 2/week |
| Money tools | 4 (budget, debt, explain, invest) | Sonnet | $0.014 avg | 0/week | 1/week |
| Relationship tools | 4 (conflict, breakup, family, friendship) | Sonnet | $0.014 avg | 0/week | 1/week |
| Journal analysis | 2 (patterns, mood) | Sonnet | $0.014 avg | 1/week | 3/week |
| Decision engine | 2 (analyze, reflect) | Sonnet | $0.014 avg | 0/week | 2/week |
| Quest system | 2 (generate, chain) | Sonnet | $0.012 avg | 0/week | 1/week |
| Life review | 2 (generate, growth) | Sonnet | $0.014 avg | 1/week | 1/week |
| Insight cards | 2 (generate, from-journal) | Sonnet | $0.006 avg | 0/week | 2/week |
| Personality training | 1 (compare — 2 API calls) | Sonnet | $0.024 | 0/month | 2/month |
| Year in review | 1 | Sonnet | $0.036 | 0/month | 1/year |
| Conversation summarize | 1 | Sonnet | $0.012 | 0/day | 1/day |
| Ecosystem sync | 2 | Sonnet | $0.012 avg | 0/month | 1/month |

## Per-User Monthly AI Costs

Notch is the most AI-intensive app — Sonnet is used for ALL non-chat features (domain tools, journal, decisions, quests, reviews).

| User Type | Calls/Month | Model | API Cost/Month |
|-----------|------------|-------|---------------|
| **Free casual** | ~40 (3 chats/day × 10 days + 1 review) | Haiku | **$0.06** |
| **Free engaged** | ~60 (maxes limit) | Haiku | **$0.10** |
| **Pro casual** | ~200 (5 chats/day + weekly tools + journal) | Haiku | **$0.30** |
| **Pro engaged** | ~500 (daily chat + domain tools + quests) | Haiku | **$0.72** |
| **Pro Max casual** | ~200 (100 Sonnet + 100 Haiku) | Sonnet+Haiku | **$2.80** |
| **Pro Max engaged** | ~600 (100 Sonnet + 500 Haiku) | Sonnet+Haiku | **$3.60** |
| **Pro Max power** | ~1,200 (100 Sonnet + 1,100 Haiku) | Sonnet+Haiku | **$4.82** |

## Revenue Streams

### 1. Subscriptions (Primary)

| Tier | Monthly Net (Y1) | Casual Cost | Casual Margin | Power Cost | Power Margin |
|------|-----------------|-------------|---------------|------------|--------------|
| Free | $0 | $0.06 | -$0.06 | $0.10 | -$0.10 |
| Pro monthly | $4.19 | $0.30 | **$3.89 (93%)** | $0.72 | **$3.47 (83%)** |
| Pro Max monthly | $6.99 | $2.80 | **$4.19 (60%)** | $4.82 | **$2.17 (31%)** |
| Student monthly | $4.19 | $0.30 | **$3.89 (93%)** | $0.72 | **$3.47 (83%)** |

### 2. Boost Packs
Notch's power users (career tools, decision engine, quest chains) will likely be the highest boost pack buyers in the portfolio. Each career tool call is a Sonnet call.

### 3. Personality Training (Unique Monetization)
- 12-question calibration with A/B comparison
- Custom overrides (never_say, always_say, tone, topic)
- Currently included in Pro. Could be standalone upsell ($2.99 one-time?) or exclusive to Pro Max.

### 4. Ecosystem Integration
- Cross-app data sync (Vinla health, Plainly finance)
- Future: unified dashboard across all Plainly Digital apps
- Potential bundle pricing: all 4 apps for $14.99/mo

### 5. Future Revenue
- Life coaching session exports (PDF reports)
- Career document generation (resumes, cover letters) as premium
- Year in Review as a shareable/printable product

## Notch Break-Even & Projections

**Break-even:** $74 ÷ $4.19 = **18 Pro monthly subscribers**

| Month | Free | Pro | Pro Max | Student | Sub MRR | Boosts | Total MRR | Net |
|-------|------|-----|---------|---------|---------|--------|-----------|-----|
| 3 | 80 | 20 | 5 | 10 | $160 | $8 | **$168** | $94 |
| 6 | 250 | 60 | 15 | 30 | $470 | $25 | **$495** | $421 |
| 12 | 800 | 180 | 40 | 80 | $1,378 | $70 | **$1,448** | $1,374 |
| 18 | 2,000 | 450 | 100 | 200 | $3,440 | $180 | **$3,620** | $3,546 |
| 24 | 5,000 | 900 | 200 | 400 | $6,879 | $350 | **$7,229** | $7,155 |

---

# PORTFOLIO SUMMARY

## Combined Revenue Projections

| Month | Plainly | Winlet | Vinla | Notch | **Portfolio MRR** | **Portfolio Net** |
|-------|---------|-------------|---------|------|------------------|------------------|
| 3 | $308 | $192 | $183 | $168 | **$851** | **$555** |
| 6 | $966 | $505 | $546 | $495 | **$2,512** | **$2,216** |
| 12 | $2,873 | $1,267 | $1,826 | $1,448 | **$7,414** | **$7,118** |
| 18 | $7,154 | $3,116 | $4,326 | $3,620 | **$18,216** | **$17,920** |
| 24 | $14,835 | $6,287 | $8,783 | $7,229 | **$37,134** | **$36,838** |

**Portfolio ARR at 24 months: ~$445K**

## Margin Analysis Summary

| Tier | Typical User Margin | Power User Margin | Risk Level |
|------|--------------------|--------------------|-----------|
| **Free** | -$0.03 to -$0.10 (loss leader) | Same | None — expected cost of acquisition |
| **Pro Monthly** | **93-96%** | **83-87%** | Very low — Haiku is cheap |
| **Pro Annual** | **90-95%** | **75-82%** | Low — locked revenue, lower per-month |
| **Pro Max Monthly** | **60-86%** | **31%** | Medium — Sonnet cap is the safety valve |
| **Pro Max Annual** | **68-79%** | **-3% to 31%** | **Higher** — power users on annual can lose money |
| **Student/Founding** | **89-91%** | **68-75%** | Low — Haiku model, lower price but lower cost |
| **Boosts** | **100% margin** (pure incremental) | Same | None — already paid for infra |

## Key Insights

### 1. Pro Tier is the Profit Engine
At 93-96% margins on casual users and 83-87% on engaged users, Pro ($5.99/mo) is the sweet spot. Haiku 4.5 is cheap enough that even heavy Pro users generate strong margins.

### 2. Pro Max is Premium, Not Profit-Maximizing
Pro Max exists to capture willingness-to-pay from power users who want Sonnet quality. The 100/mo Sonnet cap is critical — without it, power users could cost $15+/month in API fees. The Haiku fallback after 100 Sonnet calls keeps costs bounded.

### 3. Boost Packs are Pure Margin
$1.99 for 50 calls = $0.04/call revenue. Haiku costs $0.002/call. That's **95%+ margin on every boost**. Even if Pro Max users buy boosts for Sonnet calls ($0.026/call), margin is still 35%. Boosts should be actively promoted.

### 4. Plainly Has the Highest Revenue Ceiling
Affiliate revenue gives Plainly a second revenue stream that scales with users, not just subscribers. At 10K MAU, affiliate revenue ($4-6K/mo) could rival subscription revenue. No other app in the portfolio has this.

### 5. Notch Has the Highest Per-User API Cost
28+ API endpoints (all Sonnet for domain tools) makes Notch the most expensive app per active user. The standardized model (Haiku on Pro, Sonnet only on Pro Max) significantly reduces this risk vs. the current all-Sonnet approach.

### 6. The 100 Sonnet Cap is the Portfolio Safety Valve
Without the cap: a Pro Max power user doing 80 Sonnet calls/day = 2,400/month = ~$62/month in API costs (6x revenue).
With the cap: 100 Sonnet + 1,100 Haiku = ~$4.82/month. The cap makes Pro Max viable.

### 7. Fixed Costs are Negligible at Scale
$296/month for 4 apps is nothing. At 100 total paying subscribers (easily achievable), fixed costs are <5% of revenue. The business scales almost entirely on variable (API) costs.

## Risk Matrix

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Anthropic raises API prices | High | Medium | Sonnet cap limits exposure; can migrate to Haiku-only in emergency |
| Pro Max annual power users lose money | Medium | Low | Very few users max 1,200 calls/month consistently |
| Free tier costs exceed acquisition value | Low | Low | At $0.04-$0.10/user/month, 1,000 free users = $40-$100/mo |
| Apple raises store fee above 30% | High | Very Low | Regulatory trend is toward lower fees |
| Low conversion from free to paid | High | Medium | Free tier deliberately limited (5-10 calls/day) to drive upgrades |

## Bundle Opportunity

A future "Plainly Digital All-Access" bundle across all 4 apps:
- **$14.99/mo** — Pro Max on all 4 apps (vs. $39.96 if purchased separately)
- 63% discount drives adoption across the portfolio
- Cross-app ecosystem (Notch syncs with Vinla health data, Plainly finance data)
- At 500 bundle subscribers: $7,500 MRR with portfolio-level Sonnet cap (200 total across apps)

---

## Appendix: Per-Call Cost Calculation Detail

**Haiku 4.5 typical call:**
```
Input:  750 tokens × ($0.80 / 1,000,000) = $0.0006
Output: 256 tokens × ($4.00 / 1,000,000) = $0.0010
Total:  $0.0016 → rounds to $0.002
```

**Sonnet 4.6 coach chat:**
```
Input:  2,500 tokens × ($3.00 / 1,000,000) = $0.0075
Output: 512 tokens × ($15.00 / 1,000,000) = $0.0077
Total:  $0.0152 → rounds to $0.015
```

**Sonnet 4.6 long context (Notch life review, coach with history):**
```
Input:  3,500 tokens × ($3.00 / 1,000,000) = $0.0105
Output: 1,024 tokens × ($15.00 / 1,000,000) = $0.0154
Total:  $0.0259 → rounds to $0.026
```

**Worst-case Pro Max month (any app):**
```
100 Sonnet calls × $0.026 = $2.60
1,100 Haiku calls × $0.002 = $2.20
Total: $4.80
Revenue (monthly): $6.99 net
Margin: $2.19 (31%)
```
