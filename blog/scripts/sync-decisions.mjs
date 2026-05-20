#!/usr/bin/env node
/**
 * Copy archive/decisions/*.md from the repo root into the Astro content
 * collection directory before each build/dev run.
 *
 * Mirrors sync-fellows.mjs. The repo's archive/ is the source of truth;
 * Astro's content collection glob loader can't reach outside the project
 * root, so we copy in at build time. Only the kinds that belong on the
 * public /records page are copied — peer_review, curriculum_response,
 * and other research-flow events are not surfaced (they already live on
 * the post pages).
 */

import { existsSync } from 'node:fs';
import { readdir } from 'node:fs/promises';
import { join } from 'node:path';
import {
  clearDest,
  copyOne,
  ensureDir,
  readFrontmatter,
  resolvePaths,
  runSync,
} from './lib/sync.mjs';

const TAG = 'sync-decisions';

// Kinds that belong on the public /records page. Other kinds (peer_review,
// curriculum_response, proposal, revision_required, editorial,
// final_revision_required, qualifying_proposal, qualifying_publication)
// are excluded — they're research-flow events already visible elsewhere.
const PUBLIC_KINDS = new Set([
  'bootstrap',
  'admission',
  'promotion',
  'promotion_review',
  'release',
  'andon_cord_pulled',
  'andon_cord_outcome',
  'editorial_ruling',
  'charter_violation_termination',
]);

await runSync(TAG, async () => {
  const { source, dest } = resolvePaths(
    import.meta.url,
    'archive/decisions',
    'src/content/decisions',
  );

  if (!existsSync(source)) {
    console.warn(`[${TAG}] no source directory at ${source}; skipping`);
    return;
  }

  await ensureDir(dest);
  await clearDest(dest, ['.md']);

  let copied = 0;
  let skipped = 0;
  for (const entry of await readdir(source)) {
    if (!entry.endsWith('.md')) continue;
    const fm = readFrontmatter(join(source, entry));
    const kind = fm?.data?.kind ?? null;
    if (!kind) {
      throw new Error(`${entry} has no parseable frontmatter or missing 'kind'`);
    }
    if (!PUBLIC_KINDS.has(kind)) {
      skipped += 1;
      continue;
    }
    await copyOne(join(source, entry), join(dest, entry));
    copied += 1;
  }
  console.log(`[${TAG}] copied ${copied} decision(s) (skipped ${skipped} non-public)`);
});
