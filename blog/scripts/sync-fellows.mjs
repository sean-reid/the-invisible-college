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

import { existsSync } from 'node:fs';
import { readdir } from 'node:fs/promises';
import { join } from 'node:path';
import {
  clearDest,
  copyOne,
  ensureDir,
  resolvePaths,
  runSync,
} from './lib/sync.mjs';

const TAG = 'sync-fellows';

await runSync(TAG, async () => {
  const { source, dest } = resolvePaths(import.meta.url, 'genomes', 'src/content/fellows');

  if (!existsSync(source)) {
    console.warn(`[${TAG}] no source directory at ${source}; skipping`);
    return;
  }

  await ensureDir(dest);
  await clearDest(dest, ['.json']);

  let count = 0;
  for (const entry of await readdir(source)) {
    if (!entry.endsWith('.json')) continue;
    await copyOne(join(source, entry), join(dest, entry));
    count += 1;
  }
  console.log(`[${TAG}] copied ${count} genome(s) to ${dest}`);
});
