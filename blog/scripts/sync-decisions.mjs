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

import { copyFile, mkdir, readdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(here, '..', '..');
const source = join(repoRoot, 'archive', 'decisions');
const dest = join(here, '..', 'src', 'content', 'decisions');

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

if (!existsSync(source)) {
  console.warn(`[sync-decisions] no source directory at ${source}; skipping`);
  process.exit(0);
}

await mkdir(dest, { recursive: true });

for (const entry of await readdir(dest)) {
  if (entry.endsWith('.md')) await rm(join(dest, entry));
}

function frontmatterKind(text) {
  const m = text.match(/^---\n(.*?)\n---/s);
  if (!m) return null;
  for (const line of m[1].split('\n')) {
    const [k, ...rest] = line.split(':');
    if (k.trim() === 'kind') return rest.join(':').trim();
  }
  return null;
}

let copied = 0;
let skipped = 0;
for (const entry of await readdir(source)) {
  if (!entry.endsWith('.md')) continue;
  const text = readFileSync(join(source, entry), 'utf-8');
  const kind = frontmatterKind(text);
  if (!kind || !PUBLIC_KINDS.has(kind)) {
    skipped += 1;
    continue;
  }
  await copyFile(join(source, entry), join(dest, entry));
  copied += 1;
}
console.log(`[sync-decisions] copied ${copied} decision(s) (skipped ${skipped} non-public)`);
