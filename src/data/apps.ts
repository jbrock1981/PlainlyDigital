export interface IAppMeta {
  slug: string;
  name: string;
  tagline: string;
  description: string;
  status: "available" | "coming-soon" | "in-beta";
  features: string[];
  primary: string;
  primaryBg: string;
  iconSlug: string;
  legal?: {
    privacyPath: string;
    termsPath: string;
  };
}

export const APPS: IAppMeta[] = [
  {
    slug: "patet",
    name: "Patet",
    tagline: "An AI money coach that reads your real bank data.",
    description:
      "Glyphe is an AI money coach (Claude Sonnet 4.6) that reads your real Plaid transactions and uploaded bank statements, then coaches you in plain English. Spent $80 on takeout this week? Glyphe surfaces it, names the pattern, and assigns the lesson — multi-turn, in your context, not as a passive feed. 121 lessons across 18 modules supply the curriculum Glyphe draws from.",
    status: "in-beta",
    features: [
      "Glyphe AI coach (Claude Sonnet 4.6) reads your real Plaid transactions + uploaded statements and coaches in plain English",
      "AI extracts transactions from PDF / CSV / Excel statement uploads if you don't want Plaid",
      "Plaid-driven lesson assignment: AI picks the lesson that matches your actual spending pattern",
      "Money Personality, Money Roast, Future You Visualizer, weekly Money Wrapped recap — all AI-generated",
      "Curriculum layer: 121 lessons across 18 modules — budgeting, debt, investing, taxes, retirement",
      "Patet Certified™ credential — AI-graded 50-question assessment, shareable on LinkedIn",
      "Crisis routing always free, regardless of tier (Unicode-normalized text classification)",
    ],
    primary: "var(--app-patet)",
    primaryBg: "var(--app-patet-bg)",
    iconSlug: "patet",
    legal: {
      privacyPath: "/patet/privacy",
      termsPath: "/patet/terms",
    },
  },
  {
    slug: "cleardoc",
    name: "ClearDoc",
    tagline: "AI reads the document. You decide what to do.",
    description:
      "Point your camera at any confusing document — a bill, a contract, a benefits letter — and get a plain-English summary, action items, and key numbers in seconds.",
    status: "coming-soon",
    features: [
      "Camera-first capture with auto-cropping",
      "AI-powered plain-English explanation",
      "Action items + key dates extracted automatically",
      "Sensitive identifiers (SSN, card numbers) redacted on-device",
      "Account deletion in two taps — your data, your call",
    ],
    primary: "var(--app-cleardoc)",
    primaryBg: "var(--app-cleardoc-bg)",
    iconSlug: "cleardoc",
    legal: {
      privacyPath: "/cleardoc/privacy",
      termsPath: "/cleardoc/terms",
    },
  },
  {
    slug: "sittersheet",
    name: "SitterSheet",
    tagline: "An AI wizard turns your answers into a sitter guide.",
    description:
      "An AI-guided wizard turns your answers into a warm, comprehensive pet-and-house-sitter guide. Share with a 30-day expiring link or export a PDF — no apps for them to install.",
    status: "coming-soon",
    features: [
      "Wizard with per-pet feeding, meds, exercise, and quirks",
      "House info: WiFi, alarms, trash day, neighbors",
      "Sensitive fields stored on-device via Keychain / Keystore",
      "Share link expires in 30 days — rotate anytime",
      "PDF export for sitters who'd rather print it",
    ],
    primary: "var(--app-sittersheet)",
    primaryBg: "var(--app-sittersheet-bg)",
    iconSlug: "sittersheet",
    legal: {
      privacyPath: "/sittersheet/privacy",
      termsPath: "/sittersheet/terms",
    },
  },
  {
    slug: "vinla",
    name: "Vinla",
    tagline: "AI health experiments, run on your own data.",
    description:
      "Run N-of-1 health experiments on yourself with statistical rigor. Persistent AI memory, food vision, and Health Connect integration — without the wellness-industrial-complex sales pitch.",
    status: "coming-soon",
    features: [
      "N-of-1 experiments with Welch's t-test + effect size",
      "Persistent AI memory (client-side, zero-cost)",
      "Food vision (barcode + photo)",
      "Crisis routing always free",
    ],
    primary: "var(--app-vinla)",
    primaryBg: "var(--app-vinla-bg)",
    iconSlug: "vinla",
  },
  {
    slug: "winlet",
    name: "Winlet",
    tagline: "AI extracts your wins. Hype Circles celebrate them.",
    description:
      "Log daily wins (or let AI extract them from screenshots), get monthly Wrapped-style recaps, and share with a Hype Circle of people who actually want you to win.",
    status: "coming-soon",
    features: [
      "Win extraction from screenshots via vision",
      "Monthly + yearly Wrapped recaps",
      "Hype Circles for invite-only celebration",
      "Win remixes (tweet/meme/affirmation)",
    ],
    primary: "var(--app-winlet)",
    primaryBg: "var(--app-winlet-bg)",
    iconSlug: "winlet",
  },
  {
    slug: "ai-life-advisor",
    name: "Glyphe",
    tagline: "A personality-calibrated AI life advisor.",
    description:
      "Glyphe is built around a Claude-powered AI advisor that learns your values, voice, and context through a 12-question calibration, then gives the kind of advice you'd get from a wise friend who actually pays attention. Persistent memory across conversations. Year-in-review story format. In active development on Google Cloud (Cloud Run + Firebase Hosting).",
    status: "coming-soon",
    features: [
      "Personality calibration (12 questions, no quizzes)",
      "Persistent context across conversations",
      "Year-in-review story format",
      "Tiered limits — never gates crisis routing",
    ],
    primary: "var(--app-advisor)",
    primaryBg: "var(--app-advisor-bg)",
    iconSlug: "advisor",
  },
];

export function appBySlug(slug: string): IAppMeta | undefined {
  return APPS.find((a) => a.slug === slug);
}
