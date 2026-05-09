/**
 * Export every SVG in public/icons/ to a 1024x1024 PNG of the same basename.
 * Used for app store icons + apple-touch-icon.
 *
 * Run: npm run icons:build
 */
import { readFile, writeFile, readdir } from "node:fs/promises";
import { join, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";
import { Resvg } from "@resvg/resvg-js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const PUBLIC = join(__dirname, "..", "public");
const ICONS_DIR = join(PUBLIC, "icons");

async function render(svgPath, outPath, width) {
  const source = await readFile(svgPath, "utf-8");
  const renderer = new Resvg(source, {
    fitTo: { mode: "width", value: width },
    background: "transparent",
    font: { loadSystemFonts: false },
  });
  await writeFile(outPath, renderer.render().asPng());
}

const files = await readdir(ICONS_DIR);
const svgs = files.filter((f) => f.endsWith(".svg"));

for (const svg of svgs) {
  const name = basename(svg, ".svg");
  const out = join(ICONS_DIR, `${name}-1024.png`);
  await render(join(ICONS_DIR, svg), out, 1024);
  console.log(`✓ ${svg} → icons/${name}-1024.png`);
}

// Open Graph default image (1200x630)
await render(join(PUBLIC, "og-default.svg"), join(PUBLIC, "og-default.png"), 1200);
console.log(`✓ og-default.svg → og-default.png`);

// Open Graph image for Patet (1200x630)
await render(join(PUBLIC, "og-patet.svg"), join(PUBLIC, "og-patet.png"), 1200);
console.log(`✓ og-patet.svg → og-patet.png`);

console.log(`\nGenerated ${svgs.length + 2} images.`);
