// Single source of truth for company + founder facts surfaced on the
// marketing site. Update the founder name here once and it propagates to
// the About page and the homepage founder strip.

export const COMPANY = {
  legalName: "Plainly Digital LLC",
  shortName: "Plainly Digital",
  founded: 2025,
  state: "Tennessee",
  contactEmail: "apps@plainlydigital.com",
} as const;

export const FOUNDER = {
  name: "Jonathan Brock",
  role: "Founder & Principal Engineer",
  // Optional — set to a real URL to render a profile link, or leave empty.
  linkedin: "",
} as const;
