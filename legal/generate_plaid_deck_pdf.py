#!/usr/bin/env python3
"""
PDF mirror of the Patet × Plaid partnership deck.

Same content as generate_plaid_deck.py, rendered directly to PDF via
reportlab so it can be viewed without PowerPoint / LibreOffice installed.

Run:
    /tmp/docxenv/bin/python legal/generate_plaid_deck_pdf.py

Output:
    legal/PATET_PLAID_PARTNERSHIP_DECK.pdf
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "PATET_PLAID_PARTNERSHIP_DECK.pdf"

# Page geometry — match the pptx (13.333" × 7.5", widescreen)
PT_PER_IN = 72.0
PAGE_W = 13.333 * PT_PER_IN
PAGE_H = 7.5 * PT_PER_IN

# Brand colors
INK = HexColor("#0F0F0F")
PAPER = HexColor("#FFFFFF")
CHARCOAL = HexColor("#1C1C1E")
GREEN = HexColor("#10B981")
MUTED = HexColor("#6B7280")
RULE = HexColor("#E5E7EB")
GREEN_TINT = HexColor("#ECFDF5")
SOFT_BG = HexColor("#F9FAFB")
LIGHT_TEXT = HexColor("#D1D5DB")
DARKER_CARD = HexColor("#27272A")
DIM_TEXT = HexColor("#C0C0C0")
DIMMER_TEXT = HexColor("#9CA3AF")

MARGIN = 0.6 * PT_PER_IN
TOTAL_SLIDES = 12

# Default fonts — Helvetica is bundled with reportlab and renders cleanly.
FONT_REG = "Helvetica"
FONT_BOLD = "Helvetica-Bold"


# ─── Coord helpers ────────────────────────────────────────────────────────────
# Pptx uses top-left origin in inches. Reportlab uses bottom-left in points.
# These helpers let us write slide layout code in "pptx" style.

def inches(n):
    return n * PT_PER_IN


def y_from_top(top_in):
    """Convert a 'distance from top in inches' to a reportlab y coordinate."""
    return PAGE_H - top_in * PT_PER_IN


# ─── Drawing primitives ───────────────────────────────────────────────────────

def fill_rect(c, x, y_top, w, h, color):
    """Fill a rectangle. x/y_top/w/h all in points; y_top measured from page top."""
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.rect(x, PAGE_H - y_top - h, w, h, stroke=0, fill=1)


def rounded_rect(c, x, y_top, w, h, color, radius=6, stroke_color=None, stroke_w=0):
    c.setFillColor(color)
    if stroke_color and stroke_w > 0:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_w)
        c.roundRect(x, PAGE_H - y_top - h, w, h, radius, stroke=1, fill=1)
    else:
        c.setStrokeColor(color)
        c.roundRect(x, PAGE_H - y_top - h, w, h, radius, stroke=0, fill=1)


def ellipse(c, x, y_top, w, h, color):
    c.setFillColor(color)
    c.setStrokeColor(color)
    cx = x + w / 2
    cy = PAGE_H - y_top - h / 2
    c.ellipse(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, stroke=0, fill=1)


def hairline(c, x, y_top, w, color=RULE):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    y = PAGE_H - y_top
    c.line(x, y, x + w, y)


def _word_wrap(c, text, font, size, max_w):
    """Greedy wrap, returns a list of lines that each fit max_w."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = w if not cur else f"{cur} {w}"
        if c.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # If a single word exceeds width, force it on its own line
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text(c, text, x, y_top, w, *, size=14, bold=False, color=INK,
              align="left", anchor="top", h=None, leading_mult=1.25):
    """Draw possibly-wrapped text inside (x, y_top, w, h). Mirrors pptx add_text."""
    font = FONT_BOLD if bold else FONT_REG
    c.setFont(font, size)
    c.setFillColor(color)
    lines = _word_wrap(c, text, font, size, w)
    line_h = size * leading_mult
    total_h = line_h * len(lines)

    if h is not None and anchor == "middle":
        first_baseline_top = y_top + (h - total_h) / 2 + size
    elif h is not None and anchor == "bottom":
        first_baseline_top = y_top + h - total_h + size
    else:
        first_baseline_top = y_top + size

    for i, line in enumerate(lines):
        ly_top = first_baseline_top + i * line_h
        y = PAGE_H - ly_top
        if align == "right":
            c.drawRightString(x + w, y, line)
        elif align == "center":
            c.drawCentredString(x + w / 2, y, line)
        else:
            c.drawString(x, y, line)
    return total_h


def draw_bullets(c, items, x, y_top, w, *, size=12, color=INK, gap=4, leading_mult=1.25):
    """Bullet list. Green disc + body. Returns total height used."""
    cur_y = y_top
    bullet_w = c.stringWidth("•  ", FONT_BOLD, size)
    body_x = x + bullet_w
    body_w = w - bullet_w
    for item in items:
        # Wrap the body
        lines = _word_wrap(c, item, FONT_REG, size, body_w)
        line_h = size * leading_mult
        # Bullet disc on first line
        c.setFont(FONT_BOLD, size)
        c.setFillColor(GREEN)
        c.drawString(x, PAGE_H - cur_y - size, "•")
        c.setFont(FONT_REG, size)
        c.setFillColor(color)
        for i, line in enumerate(lines):
            ly = cur_y + i * line_h
            c.drawString(body_x, PAGE_H - ly - size, line)
        cur_y += line_h * len(lines) + gap
    return cur_y - y_top


# ─── Common chrome ────────────────────────────────────────────────────────────

def slide_header(c, eyebrow, title, *, eyebrow_color=GREEN):
    draw_text(
        c, eyebrow.upper(), MARGIN, inches(0.5), PAGE_W - 2 * MARGIN,
        size=11, bold=True, color=eyebrow_color,
    )
    draw_text(
        c, title, MARGIN, inches(0.85), PAGE_W - 2 * MARGIN,
        size=28, bold=True, color=INK,
    )
    hairline(c, MARGIN, inches(1.85), PAGE_W - 2 * MARGIN)


def slide_footer(c, slide_num):
    draw_text(
        c, "Patet · Plainly Digital LLC",
        MARGIN, inches(7.15), inches(5), size=9, color=MUTED,
    )
    draw_text(
        c, f"{slide_num} / {TOTAL_SLIDES}",
        PAGE_W - MARGIN - inches(1), inches(7.15), inches(1),
        size=9, color=MUTED, align="right",
    )


# ─── Slides ───────────────────────────────────────────────────────────────────

def slide_01_title(c):
    fill_rect(c, 0, 0, PAGE_W, PAGE_H, CHARCOAL)
    fill_rect(c, inches(0.6), inches(2.6), inches(0.18), inches(1.6), GREEN)
    draw_text(c, "PATET", inches(1.0), inches(2.55), inches(10),
              size=52, bold=True, color=PAPER)
    draw_text(
        c,
        "Money skills + your real bank data + an AI coach who knows what you're actually spending on.",
        inches(1.0), inches(3.85), inches(11.3),
        size=20, color=PAPER,
    )
    draw_text(
        c, "Plaid IAM partnership briefing  ·  prepared May 2026",
        inches(1.0), inches(5.0), inches(11.3),
        size=13, color=DIM_TEXT,
    )
    draw_text(
        c,
        "Plainly Digital LLC  ·  Operator: Jonathan Brock, Managing Member  ·  plainlydigital.com",
        inches(0.6), inches(7.15), inches(12),
        size=10, color=DIMMER_TEXT,
    )


def slide_02_thesis(c):
    slide_header(c, "The thesis",
                 "Three forces are converging. Patet sits exactly in the middle.")
    col_w = inches(3.95)
    gap = inches(0.25)
    col_top = inches(2.3)
    col_h = inches(4.4)
    headlines = [
        ("01", "AI quality crossed the line", [
            "Frontier LLMs (Claude Sonnet, GPT-4o) can answer real personal-finance questions accurately and on-budget.",
            "Inference cost has fallen >50% YoY — viable at sub-$3 MRR.",
            "Coach-style products (Cleo, Origin) have validated demand.",
        ]),
        ("02", "Mint left a vacuum", [
            "Intuit shut Mint down March 2024. ~20M users displaced.",
            "Premium replacements (Monarch, Copilot) cost $13-$15/mo. None ship a curriculum.",
            "The free-tier hole is wide open below $5/mo.",
        ]),
        ("03", "Gen Z is unbanked on knowledge", [
            "Only 24% of Gen Z feel confident managing money. 36% find finance confusing.",
            "Gen Z gamified-literacy market: $0.31B (2025) -> $1.92B (2034), 22.9% CAGR.",
            "No incumbent owns this segment with both bank data + curriculum.",
        ]),
    ]
    x = MARGIN
    for label, head, lines in headlines:
        rounded_rect(c, x, col_top, col_w, col_h, GREEN_TINT, radius=10)
        draw_text(c, label, x + inches(0.3), col_top + inches(0.25),
                  inches(2), size=14, bold=True, color=GREEN)
        draw_text(c, head, x + inches(0.3), col_top + inches(0.7),
                  col_w - inches(0.6), size=17, bold=True, color=INK)
        draw_bullets(c, lines, x + inches(0.3), col_top + inches(1.9),
                     col_w - inches(0.6), size=11, color=INK)
        x += col_w + gap
    slide_footer(c, 2)


def slide_03_market(c):
    slide_header(c, "Market context",
                 "A real category, an underserved sub-segment, an obvious wedge.")
    left_x = MARGIN
    left_w = inches(6.4)
    draw_text(c, "The category is real, the entry tier is empty.",
              left_x, inches(2.2), left_w, size=17, bold=True, color=INK)
    bullets = [
        "Personal-finance software TAM: $1.08B (2022) -> $1.59B (2030), 5.1% CAGR. Source: Grand View Research.",
        "Broader personal-finance-apps market projected $207B (2026) -> $507B (2030). Source: Business Research Company.",
        "Gen Z gamified-literacy subsegment is the fastest-growing slice: 22.9% CAGR to 2034.",
        "Mint shutdown (Mar 2024) -> ~20M users displaced. Monarch absorbed ~1M (April 2026, $850M valuation, $75M Series B).",
        "Rocket Money grew to 10M+ members post-Mint. Copilot Money grew to 100K+ paying.",
        "Median competitor Pro tier price: $12.99/mo. Median annual: ~$95. Patet enters at $2.99 / $6.99.",
    ]
    draw_bullets(c, bullets, left_x, inches(2.95), left_w, size=12)

    right_x = inches(7.2)
    right_w = PAGE_W - right_x - MARGIN
    card_top = inches(2.2)
    card_h = inches(4.6)
    rounded_rect(c, right_x, card_top, right_w, card_h, CHARCOAL, radius=12)
    draw_text(c, "The gap, in one sentence",
              right_x + inches(0.35), card_top + inches(0.3),
              right_w - inches(0.7), size=12, bold=True, color=GREEN)
    draw_text(
        c,
        "No competitor in the US market bundles a structured financial-literacy curriculum, live bank data, and a real LLM coach in a single product priced under $7/month.",
        right_x + inches(0.35), card_top + inches(0.85),
        right_w - inches(0.7), size=16, bold=True, color=PAPER,
    )
    draw_text(
        c,
        "Cleo has personality but no curriculum. Origin has SEC-regulated AI but no lessons and $13/mo entry. Ramsey has curriculum but no AI or live bank data. YNAB has bank data but no AI, no lessons, and a $15/mo floor.",
        right_x + inches(0.35), card_top + inches(3.0),
        right_w - inches(0.7), size=11, color=DIM_TEXT,
    )
    slide_footer(c, 3)


def slide_04_one_screen(c):
    slide_header(c, "The product", "What ships today — one screen.")
    metrics = [("18", "modules"), ("121", "lessons"),
               ("36+", "screens"), ("EN / ES", "languages")]
    strip_top = inches(2.2)
    strip_h = inches(1.4)
    col_w = (PAGE_W - 2 * MARGIN - inches(0.6)) / 4
    x = MARGIN
    for big, small in metrics:
        rounded_rect(c, x, strip_top, col_w, strip_h, GREEN_TINT, radius=10)
        draw_text(c, big, x, strip_top + inches(0.25), col_w,
                  size=28, bold=True, color=GREEN, align="center")
        draw_text(c, small, x, strip_top + inches(0.95), col_w,
                  size=12, color=INK, align="center")
        x += col_w + inches(0.2)

    col_top = inches(3.95)
    col_w3 = (PAGE_W - 2 * MARGIN - inches(0.4)) / 3
    cols = [
        ("Curriculum", [
            "18 modules · 121 lessons (~2-5 min each)",
            "242 quiz cards, 50-question final assessment",
            "Modules incl. Paycheck, Debt, Saving, Budgeting, Investing, Credit, Student Loans, Mental-Health-of-money",
            "Spanish parity shipped (LATAM reviewer pass pending)",
        ]),
        ("AI coach (Glyphe)", [
            "Claude Sonnet 4.6 (Coached) + Haiku 4.5 (Free/Connected)",
            "Knows your 121 lessons + 11 affiliate products + your Plaid spending",
            "4 personas unlocked by progress: Older Sibling -> Strategist -> Therapist -> Hype Friend",
            "Voice in/out · streaming · follow-up chips",
            "Crisis detection + medical/legal/financial guardrails",
        ]),
        ("Bank data + tools", [
            "Plaid Link (Transactions + Liabilities), encrypted tokens (AES-256-GCM)",
            "Statement upload — PDF / CSV / Excel, AI-extracted transactions",
            "5 calculators, What-If scenarios, Future You, Money Roast, Money IQ, Salary negotiation",
            "Spending-pattern detection -> ranked lesson recs",
            "Peer benchmarks (20-user minimum cohort, k-anonymity)",
        ]),
    ]
    x = MARGIN
    for title, lines in cols:
        draw_text(c, title, x, col_top, col_w3,
                  size=14, bold=True, color=INK)
        draw_bullets(c, lines, x, col_top + inches(0.45), col_w3, size=10)
        x += col_w3 + inches(0.2)
    slide_footer(c, 4)


def slide_05_moat(c):
    slide_header(c, "The moat", "Three layers, no competitor has all three.")
    diagram_top = inches(2.3)
    boxes = [
        (inches(2.1), diagram_top + inches(0.0), "Curriculum",
         "18 modules · 121 lessons · cert exam"),
        (inches(7.6), diagram_top + inches(0.0), "Live bank data",
         "Plaid + statement upload · 90d history"),
        (inches(4.85), diagram_top + inches(2.2), "AI coach",
         "Claude Sonnet / Haiku · spending-aware"),
    ]
    for x, top, head, sub in boxes:
        rounded_rect(c, x, top, inches(3.6), inches(1.5), PAPER,
                     radius=10, stroke_color=GREEN, stroke_w=2)
        draw_text(c, head, x, top + inches(0.3), inches(3.6),
                  size=18, bold=True, color=INK, align="center")
        draw_text(c, sub, x, top + inches(0.85), inches(3.6),
                  size=11, color=MUTED, align="center")

    # center oval
    ellipse(c, inches(5.55), diagram_top + inches(1.5), inches(2.2), inches(1.2), GREEN)
    draw_text(c, "PATET", inches(5.55), diagram_top + inches(1.85),
              inches(2.2), size=22, bold=True, color=PAPER, align="center")

    caption = ("Ramsey owns curriculum but has no AI and no real-time bank data. "
               "Cleo owns the AI coach but has no curriculum. Monarch / Rocket / "
               "Copilot own bank data but ship no lessons and no LLM coach. "
               "Patet is the only product at the intersection.")
    draw_text(c, caption, MARGIN, inches(6.1), PAGE_W - 2 * MARGIN,
              size=12, color=INK, align="center")
    slide_footer(c, 5)


def slide_06_competitive_matrix(c):
    slide_header(c, "Competitive landscape", "Where everyone sits — and where the gaps are.")
    headers = ["Product", "Monthly $", "LLM coach", "Plaid",
               "Curriculum", "Stmt upload", "Voice"]
    rows = [
        ("Patet",      "$2.99 / $6.99", "Yes (Sonnet+Haiku)", "Yes",          "Yes (121 lessons)",  "Yes (PDF/CSV/XLS)", "Yes"),
        ("YNAB",       "$14.99",        "No",                 "Yes",          "Workshops only",     "CSV only",          "No"),
        ("Rocket",     "$7-$14",        "No",                 "Yes",          "No",                 "No",                "No"),
        ("Copilot",    "$13",           "Partial (ML)",       "Yes",          "No",                 "CSV only",          "No"),
        ("Monarch",    "$14.99",        "No",                 "Yes",          "No",                 "CSV only",          "No"),
        ("EveryDollar","$17.99",        "No",                 "Premium only", "Ramsey FPU video",   "No",                "No"),
        ("Cleo",       "$5.99-$14.99",  "Yes (multi-model)",  "Yes",          "No",                 "No",                "Limited"),
        ("Origin",     "$12.99",        "Yes (SEC-reg)",      "Yes",          "No",                 "CSV only",          "No"),
    ]
    table_left = MARGIN
    table_top = inches(2.25)
    col_widths = [inches(1.6), inches(1.6), inches(2.1), inches(1.3),
                  inches(2.2), inches(2.0), inches(1.3)]
    row_h = inches(0.5)
    header_h = inches(0.45)

    # Header row
    x = table_left
    for i, h in enumerate(headers):
        fill_rect(c, x, table_top, col_widths[i], header_h, CHARCOAL)
        draw_text(c, h, x + inches(0.1), table_top, col_widths[i] - inches(0.2),
                  size=11, bold=True, color=PAPER, anchor="middle", h=header_h)
        x += col_widths[i]

    y = table_top + header_h
    for ri, row in enumerate(rows):
        x = table_left
        is_patet = row[0] == "Patet"
        bg = GREEN_TINT if is_patet else (SOFT_BG if ri % 2 == 0 else PAPER)
        for ci, val in enumerate(row):
            fill_rect(c, x, y, col_widths[ci], row_h, bg)
            bold = is_patet or ci == 0
            draw_text(c, val, x + inches(0.1), y,
                      col_widths[ci] - inches(0.2),
                      size=10, bold=bold, color=INK, anchor="middle", h=row_h)
            x += col_widths[ci]
        y += row_h

    draw_text(
        c,
        "Patet is the only row that says Yes across LLM coach, Plaid, curriculum, statement upload, and voice — at the lowest price point. Verified May 2026 via vendor pricing pages.",
        MARGIN, inches(6.7), PAGE_W - 2 * MARGIN,
        size=10, color=MUTED, align="center",
    )
    slide_footer(c, 6)


def slide_07_unique(c):
    slide_header(c, "Unique features", "What we ship that nobody else does.")
    diffs = [
        ("Spending-aware AI coach",
         "Claude Sonnet 4.6 with your real Plaid transactions in-context. Not a chatbot — a coach that can say 'you spent $340 on restaurants this month; here's lesson 4.3.'"),
        ("Statement upload, multi-format",
         "PDF, CSV, and Excel bank statements parsed and AI-categorized. Most competitors offer CSV only — or no upload at all."),
        ("121-lesson curriculum at $2.99",
         "Ramsey charges $79.99/year for curriculum alone. Patet ships 18 modules + 121 lessons in the $2.99/mo Connected tier — and unlocks an AI tutor that knows the curriculum cold."),
        ("Learn-then-unlock coach personas",
         "Four coach personalities unlock at module milestones (Older Sibling default -> Strategist @5 -> Therapist @10 -> Hype Friend @15). Gamifies completion."),
        ("Money Roast + Future You + Personality",
         "Emotional engagement layer competitors don't ship. Roast = 3-tone spending critique. Future You = life at 30. Personality = 5 archetypes."),
        ("Voice in / voice out",
         "Native Web Speech on web; expo-speech on mobile. Full voice-mode conversation. Cleo has voice; no other competitor in the matrix does."),
        ("Crisis detection with text normalization",
         "Unicode + homoglyph + l33tspeak normalization on every coach turn. Routes to 988 / Crisis Text Line / 211.org. NIST AI RMF aligned."),
        ("Top-of-funnel viral assessment",
         "Public Financial IQ quiz at /iq (no auth, dynamic OG share image). Free funnel that converts to registered users."),
        ("Spanish curriculum (LATAM)",
         "All 121 lessons + content surfaces translated to LATAM Spanish. Native reviewer pass pending pre-launch. No major US competitor ships Spanish curriculum."),
        ("Strict-freemium tier gating",
         "Plaid + statement upload + advanced calculators + scenarios all sit behind the $2.99 Connected tier. Hard-gated server-side, not trial-and-revoke. Real boundary."),
    ]
    col_top = inches(2.15)
    col_w = (PAGE_W - 2 * MARGIN - inches(0.4)) / 2
    row_h = inches(0.95)
    for i, (head, body) in enumerate(diffs):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + inches(0.4))
        y = col_top + row * row_h
        ellipse(c, x, y + inches(0.05), inches(0.32), inches(0.32), GREEN)
        draw_text(c, f"{i + 1:02d}", x, y + inches(0.13),
                  inches(0.32), size=9, bold=True, color=PAPER, align="center")
        draw_text(c, head, x + inches(0.45), y, col_w - inches(0.45),
                  size=12, bold=True, color=INK)
        draw_text(c, body, x + inches(0.45), y + inches(0.3),
                  col_w - inches(0.45), size=9, color=MUTED)
    slide_footer(c, 7)


def slide_08_pricing(c):
    slide_header(c, "Pricing", "Below every competitor's flagship paid tier — by 75%.")
    left_x = MARGIN
    chart_w = inches(7.0)
    chart_top = inches(2.3)
    chart_h = inches(4.4)
    rounded_rect(c, left_x, chart_top, chart_w, chart_h, SOFT_BG, radius=10)

    bars = [
        ("EveryDollar", 17.99, MUTED), ("YNAB", 14.99, MUTED),
        ("Monarch", 14.99, MUTED), ("Cleo Builder", 14.99, MUTED),
        ("Albert", 14.99, MUTED), ("Origin", 12.99, MUTED),
        ("Copilot", 13.00, MUTED), ("PocketGuard", 12.99, MUTED),
        ("Goodbudget", 10.00, MUTED), ("Rocket Money", 9.99, MUTED),
        ("Cleo Plus", 5.99, MUTED), ("Patet Coached", 6.99, GREEN),
        ("Patet Connected", 2.99, GREEN),
    ]
    competitors = [b for b in bars if not b[0].startswith("Patet")]
    competitors.sort(key=lambda b: -b[1])
    patet_rows = [b for b in bars if b[0].startswith("Patet")]
    ordered = competitors + patet_rows

    max_price = 20.0
    row_h = inches(0.27)
    row_gap = inches(0.03)
    chart_inner_top = chart_top + inches(0.3)
    label_w = inches(1.6)
    bar_left = left_x + inches(0.4) + label_w + inches(0.1)
    bar_max_w = chart_w - (bar_left - left_x) - inches(1.0)

    for i, (name, price, color) in enumerate(ordered):
        y = chart_inner_top + i * (row_h + row_gap)
        is_patet = name.startswith("Patet")
        draw_text(c, name, left_x + inches(0.4), y, label_w,
                  size=10, bold=is_patet,
                  color=INK if is_patet else MUTED,
                  anchor="middle", align="right", h=row_h)
        bar_w = bar_max_w * (price / max_price)
        fill_rect(c, bar_left, y + 3, bar_w, row_h - 6, color)
        draw_text(c, f"${price:.2f}",
                  bar_left + bar_w + 4, y, inches(0.9),
                  size=10, bold=is_patet,
                  color=GREEN if is_patet else MUTED,
                  anchor="middle", h=row_h)

    right_x = inches(7.8)
    right_w = PAGE_W - right_x - MARGIN
    draw_text(c, "What this funds", right_x, inches(2.3), right_w,
              size=17, bold=True, color=INK)
    draw_bullets(c, [
        "Free: 10 coach calls/day on Haiku 4.5. Full curriculum.",
        "Connected $2.99: Plaid, statement upload, all calculators, scenarios, credit tracker, 40 coach calls/day.",
        "Coached $6.99: 80 coach calls/day, Claude Sonnet 4.6 (50/mo cap then Haiku fallback), 1,200/mo.",
        "Annual: Connected $24.99 (saves 31%) · Coached $57.99 (saves 31%).",
        "$19 one-time IAP: Patet Certified credential with LinkedIn add-to-profile.",
        "Boost packs: +50 calls $1.99 · +200 calls $4.99.",
    ], right_x, inches(2.95), right_w, size=11)
    slide_footer(c, 8)


def slide_09_plaid_core(c):
    slide_header(c, "Why Plaid is core, not bolt-on",
                 "Plaid powers half of Patet's product surface. Removing it would gut Pro.")
    draw_text(c, "Plaid-dependent features", MARGIN, inches(2.2),
              inches(6), size=16, bold=True, color=INK)
    draw_bullets(c, [
        "Bank-account linking via Plaid Link (MFA-gated client + server)",
        "Transaction sync (Transactions product, 90-day history + ongoing webhooks)",
        "Liabilities sync (credit cards, student loans, mortgages, auto loans)",
        "Spending-pattern detection (5 pattern types) -> ranked lesson recommendations",
        "Peer benchmarks (anonymized, k>=20 cohort minimum)",
        "Coach context: every AI coach turn has Plaid spending data injected into the system prompt",
        "Spending alert notifications (threshold + category-based, deep-linkable)",
        "Webhook real-time updates (ES256 JWT verified, request_body_sha256 claim verified)",
    ], MARGIN, inches(2.7), inches(6), size=11)

    right_x = inches(7.0)
    right_w = PAGE_W - right_x - MARGIN
    card_top = inches(2.2)
    card_h = inches(4.6)
    rounded_rect(c, right_x, card_top, right_w, card_h, CHARCOAL, radius=12)
    draw_text(c, "Plaid posture", right_x + inches(0.35),
              card_top + inches(0.25), right_w - inches(0.7),
              size=12, bold=True, color=GREEN)

    posture = [
        ("Products in use",
         "Transactions, Liabilities · US country code only."),
        ("Security",
         "Plaid access tokens encrypted at rest (AES-256-GCM, dual-write to *_encrypted columns, migration 017)."),
        ("Access gate",
         "MFA enforced before /api/plaid/link-token. Email-verified required. 5-min step-up window for Plaid Link replay."),
        ("Webhook verification",
         "ES256 JWT signature, fetched per kid via webhookVerificationKeyGet, JWK->PEM via Node crypto, 5-min replay window."),
        ("Off-boarding",
         "Bank disconnect calls Plaid itemRemove first, then deletes local row. CASCADE on account deletion."),
    ]
    cy = card_top + inches(0.7)
    for head, body in posture:
        draw_text(c, head, right_x + inches(0.35), cy,
                  right_w - inches(0.7), size=11, bold=True, color=PAPER)
        cy += inches(0.28)
        h = draw_text(c, body, right_x + inches(0.35), cy,
                      right_w - inches(0.7), size=10, color=LIGHT_TEXT,
                      leading_mult=1.3)
        cy += h + inches(0.15)
    slide_footer(c, 9)


def slide_10_security(c):
    slide_header(c, "Security & compliance",
                 "We've already done the work most pre-seed startups skip.")
    items = [
        ("Authentication", [
            "TOTP MFA (AES-256-GCM secret · SHA-256-HMAC recovery codes · 10 codes, single-use)",
            "MFA enforced as a hard gate before Plaid Link (5-min step-up)",
            "Account lockout (DB-persisted, survives Render redeploys)",
            "JWT revocation by jti (migration 016)",
            "httpOnly + sameSite cookies on web; Bearer header on mobile",
        ]),
        ("Data protection", [
            "AES-256-GCM at rest on Plaid tokens, financial PII, MFA secrets",
            "Annual encryption-key rotation procedure documented (InfoSec section 7)",
            "Self-serve user data export (GET /api/auth/me/export, JSON, redactions enforced)",
            "Right-to-erasure: DELETE /api/auth/me · FK ON DELETE CASCADE across 30+ child tables",
            "Backups: Neon 7-day window, age out aligned with EDPB 06/2020",
        ]),
        ("Governance & audit", [
            "RBAC (user / support / admin) · system_audit_log table · per-session inventory",
            "NIST AI RMF-aligned audit on every AI coach turn",
            "Crisis detection: Unicode, homoglyph, l33tspeak normalization",
            "Input + output guardrails (prompt injection, role override, medical/legal/financial boundary checks)",
            "1,043 tests across the stack (632 app · 411 server)",
        ]),
        ("Policy library (LLC repo)", [
            "Information Security Policy",
            "Access Control Policy (Plaid-evidence ready)",
            "Data Retention and Disposal Policy (added 2026-05-17 for Plaid IAM Q11)",
            "Privacy Policy live at plainlydigital.com/patet/privacy",
            "Plaid form answers reference packet (PLAID_FORM_ANSWERS.md)",
        ]),
    ]
    col_w = (PAGE_W - 2 * MARGIN - inches(0.3)) / 2
    row_h = inches(2.3)
    starting_top = inches(2.15)
    for i, (title, lines) in enumerate(items):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + inches(0.3))
        y = starting_top + row * row_h
        draw_text(c, title, x, y, col_w, size=13, bold=True, color=GREEN)
        draw_bullets(c, lines, x, y + inches(0.45), col_w, size=10)
    slide_footer(c, 10)


def slide_11_roadmap(c):
    slide_header(c, "What's next", "Six-month roadmap, in order of confidence.")
    items = [
        ("Now -> Month 1", "Consumer launch",
         "Patet ships strict-freemium to public (live as of 2026-05-16). RevenueCat entitlements + Plaid prod creds + Resend transactional email all wired this week. App Store + Play Store submission queued."),
        ("Month 1 -> 3", "Affiliate revenue layer",
         "11 affiliate partners across 7 categories (Self, SoFi, Marcus, YNAB, Fidelity, Discover, Ally, Chime, Wealthfront, Lemonade, Schwab). ROAS dashboard live at /api/admin/affiliate/roas. Per-partner conversion webhooks live."),
        ("Month 2 -> 6", "Patet Certified",
         "50-question final assessment shipped. $19 one-time IAP via RevenueCat. LinkedIn add-to-profile URL helper. Vanity slug picker. Public verify endpoint. Credential as a B2B credential layer for community-college + NACFC coach licensing."),
        ("Month 3 -> 6", "LATAM launch",
         "Spanish lesson content shipped (machine-translated via Sonnet, native reviewer pass pending). 100% i18n parity test-enforced. Expansion candidates: Mexico, Colombia, Argentina."),
        ("Month 4 -> 6", "B2B curriculum licensing",
         "NACFC coach pilot (financial coaches license Patet curriculum for their clients). Community-college pilot. Employer benefits pilot via SHRM expo channel."),
        ("Month 6+", "GCP migration",
         "Move backend off Render onto Cloud Run + Cloud SQL. Cloud Build CI on push. Already migrated other Plainly Digital products; Patet is on the queue."),
    ]
    top = inches(2.15)
    row_h = inches(0.78)
    col_when_w = inches(2.0)
    col_what_w = inches(2.8)
    col_body_w = PAGE_W - 2 * MARGIN - col_when_w - col_what_w - inches(0.3)
    for i, (when, what, body) in enumerate(items):
        y = top + i * row_h
        rounded_rect(c, MARGIN, y + inches(0.1), col_when_w, inches(0.45),
                     GREEN_TINT, radius=8)
        draw_text(c, when, MARGIN, y + inches(0.22), col_when_w,
                  size=10, bold=True, color=GREEN, align="center")
        draw_text(c, what, MARGIN + col_when_w + inches(0.15),
                  y + inches(0.18), col_what_w,
                  size=13, bold=True, color=INK)
        draw_text(c, body,
                  MARGIN + col_when_w + col_what_w + inches(0.3),
                  y + inches(0.1), col_body_w,
                  size=9, color=MUTED)
    slide_footer(c, 11)


def slide_12_close(c):
    fill_rect(c, 0, 0, PAGE_W, PAGE_H, CHARCOAL)
    fill_rect(c, inches(0.6), inches(2.4), inches(0.18), inches(2.4), GREEN)
    draw_text(c, "Thanks for partnering with us.",
              inches(1.0), inches(2.4), inches(11.3),
              size=36, bold=True, color=PAPER)
    draw_text(
        c,
        "Plaid is the load-bearing partner in the most differentiated half of our product. We are building this slowly and carefully — security, governance, and customer trust first. Happy to walk through any specific area in more depth.",
        inches(1.0), inches(3.5), inches(11.3),
        size=14, color=LIGHT_TEXT,
    )
    contact_x = inches(1.0)
    contact_y = inches(5.4)
    contact_w = inches(11.3)
    rounded_rect(c, contact_x, contact_y, contact_w, inches(1.4),
                 DARKER_CARD, radius=12)
    draw_text(c, "Plainly Digital LLC  ·  DBA Patet",
              contact_x + inches(0.4), contact_y + inches(0.25),
              contact_w - inches(0.8), size=14, bold=True, color=PAPER)
    draw_text(c, "Operator: Jonathan Brock, Managing Member",
              contact_x + inches(0.4), contact_y + inches(0.6),
              contact_w - inches(0.8), size=12, color=PAPER)
    draw_text(c, "apps@plainlydigital.com  ·  support@plainlydigital.com  ·  plainlydigital.com/patet",
              contact_x + inches(0.4), contact_y + inches(0.95),
              contact_w - inches(0.8), size=12, color=PAPER)
    draw_text(c, f"12 / {TOTAL_SLIDES}",
              PAGE_W - MARGIN - inches(1), inches(7.15), inches(1),
              size=9, color=MUTED, align="right")


# ─── Build ────────────────────────────────────────────────────────────────────

def build():
    c = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Patet × Plaid partnership briefing")
    c.setAuthor("Plainly Digital LLC")
    c.setSubject("Plaid IAM partnership briefing — Patet")

    builders = [
        slide_01_title, slide_02_thesis, slide_03_market, slide_04_one_screen,
        slide_05_moat, slide_06_competitive_matrix, slide_07_unique,
        slide_08_pricing, slide_09_plaid_core, slide_10_security,
        slide_11_roadmap, slide_12_close,
    ]
    for fn in builders:
        fn(c)
        c.showPage()

    c.save()
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
