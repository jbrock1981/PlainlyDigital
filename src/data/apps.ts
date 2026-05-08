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
    slug: "cleardoc",
    name: "ClearDoc",
    tagline: "Snap it. Understand it. Act on it.",
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
    tagline: "Everything your sitter needs. One link.",
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
    slug: "plainly",
    name: "Plainly",
    tagline: "Financial literacy for Gen Z, in your voice.",
    description:
      "Bite-sized, interactive lessons on budgeting, investing, debt, taxes, and more — paired with an AI coach that adapts to where you are, not where finance bros assume you should be.",
    status: "coming-soon",
    features: [
      "Curriculum across 18 modules",
      "AI coach calibrated to your background and goals",
      "Real-time bank account integration",
      "Crisis features (overdraft help, scam recognition) always free",
    ],
    primary: "var(--app-plainly)",
    primaryBg: "var(--app-plainly-bg)",
    iconSlug: "plainly",
  },
  {
    slug: "vinla",
    name: "Vinla",
    tagline: "Track your health like a scientist.",
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
    slug: "accomplishly",
    name: "Accomplishly",
    tagline: "Celebrate your wins. Then remix them.",
    description:
      "Log daily wins (or let AI extract them from screenshots), get monthly Wrapped-style recaps, and share with a Hype Circle of people who actually want you to win.",
    status: "coming-soon",
    features: [
      "Win extraction from screenshots via vision",
      "Monthly + yearly Wrapped recaps",
      "Hype Circles for invite-only celebration",
      "Win remixes (tweet/meme/affirmation)",
    ],
    primary: "var(--app-accomplishly)",
    primaryBg: "var(--app-accomplishly-bg)",
    iconSlug: "accomplishly",
  },
  {
    slug: "ai-life-advisor",
    name: "AI Life Advisor",
    tagline: "A personal advisor that gets to know you.",
    description:
      "An AI that learns your values, your voice, and your context — then gives the kind of advice you'd get from a wise friend who actually pays attention. Name pending.",
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
