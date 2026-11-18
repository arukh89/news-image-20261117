// Entry program for make.fun news-image-20261117 (Node 22, stdlib only).
// Writes the pre-drawn entry image to /output/entry.png. The image itself
// was drawn by render.py (Pillow, build-time only) from verified reports of
// Tuesday 17 November 2026; this program only copies those exact bytes, so
// every run writes identical output with no network and no randomness.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

// The output filename stays entry.png: the gate tells PNG from JPEG by the
// first bytes, and these bytes are a PNG (1024x1024, under 1 MiB).
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });
copyFileSync(
  new URL("./entry.png", import.meta.url),
  join(outputDir, "entry.png"),
);
