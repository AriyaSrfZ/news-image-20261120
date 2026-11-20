// news-image-20261120 — entry program (Node 22, standard library only).
//
// The image is drawn by draw.py (Pillow, run at build time) and shipped as
// entry.png beside this file. The grader runs this program with no network
// in a fresh container; all it has to do is place the image at
// /output/entry.png, byte for byte, on both of its two runs.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
