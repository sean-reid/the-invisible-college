#!/usr/bin/env node
/**
 * Copy genomes/*.json from the repo root into the Astro content collection
 * directory before each build/dev run.
 *
 * Astro's content collection glob loader does not reach outside the
 * project root, so we cannot point it directly at ../genomes. Instead we
 * keep the genomes/ directory as the source of truth (committed,
 * versioned, updated by the orchestrator's bootstrap/admissions
 * workflows) and copy into the Astro project at every build.
 */

import { copyFile, mkdir, readdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..', '..');
const source = join(repoRoot, 'genomes');
const dest = join(here, '..', 'src', 'content', 'fellows');

if (!existsSync(source)) {
  console.warn(`[sync-fellows] no source directory at ${source}; skipping`);
  process.exit(0);
}

await mkdir(dest, { recursive: true });

// Clear destination json files so deleted fellows don't linger.
for (const entry of await readdir(dest)) {
  if (entry.endsWith('.json')) {
    await rm(join(dest, entry));
  }
}

let count = 0;
for (const entry of await readdir(source)) {
  if (!entry.endsWith('.json')) continue;
  await copyFile(join(source, entry), join(dest, entry));
  count += 1;
}
console.log(`[sync-fellows] copied ${count} genome(s) to ${dest}`);
