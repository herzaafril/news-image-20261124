// Entry program for the make.fun news-image bounty (24 November 2026).
//
// The image itself is drawn by draw.py (PIL, no network, deterministic).
// This program only validates the finished entry.png and copies it to the
// output directory the harness expects.
//
// Layout:
//   <bot dir>/entry.png   ->   <output dir>/entry.png
// Directories come from MAKEFUN_BOT_DIR / MAKEFUN_OUTPUT_DIR, defaulting
// to /bot and /output.
import { copyFile, mkdir, open, stat } from "node:fs/promises";
import { join } from "node:path";

const MAX_BYTES = 1024 * 1024; // 1 MiB, per the bounty rules
const MAX_DIM = 1024; // max width/height in pixels, per the bounty rules
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

async function main(): Promise<void> {
  const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const src = join(botDir, "entry.png");
  const dst = join(outDir, "entry.png");

  const info = await stat(src).catch(() => {
    throw new Error(`entry image not found at ${src}`);
  });
  if (!info.isFile()) throw new Error(`${src} is not a file`);
  if (info.size === 0) throw new Error(`${src} is empty`);
  if (info.size > MAX_BYTES) {
    throw new Error(`${src} is ${info.size} bytes, over the 1 MiB limit`);
  }

  // Read just the header: 8 magic bytes + IHDR chunk (width/height).
  const handle = await open(src, "r");
  try {
    const header = Buffer.alloc(24);
    const { bytesRead } = await handle.read(header, 0, 24, 0);
    if (bytesRead < 24) throw new Error(`${src} is too short to be a PNG`);
    if (!header.subarray(0, 8).equals(PNG_MAGIC)) {
      throw new Error(`${src} does not start with PNG magic bytes`);
    }
    const width = header.readUInt32BE(16);
    const height = header.readUInt32BE(20);
    if (width > MAX_DIM || height > MAX_DIM) {
      throw new Error(`${src} is ${width}x${height}, over the 1024x1024 limit`);
    }
    console.log(`entry image OK: ${width}x${height}, ${info.size} bytes`);
  } finally {
    await handle.close();
  }

  await mkdir(outDir, { recursive: true });
  await copyFile(src, dst);
  console.log(`copied ${src} (${info.size} bytes) -> ${dst}`);
}

await main();
