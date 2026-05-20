/**
 * Shared helpers for the sync-* scripts.
 *
 * Each sync-* script copies a slice of the repo-root archive into the
 * blog's Astro content collection directory because Astro's glob loader
 * cannot reach outside the project root. The helpers here standardise
 * three things every sync script needs:
 *
 *  - Resolving the repo root and the script's source/dest directories
 *  - Wiping the destination so deletions in the source propagate
 *  - Catching errors and exiting non-zero so a broken sync fails the
 *    build instead of silently shipping a stale or partial content
 *    collection.
 */

import { copyFile, mkdir, readdir, rm } from 'node:fs/promises';
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

/**
 * Resolve paths for a sync script. Pass `import.meta.url` from the caller
 * so the helper can locate the repo root relative to `blog/scripts/`.
 */
export function resolvePaths(metaUrl, sourceRel, destRel) {
  const here = dirname(fileURLToPath(metaUrl));
  // Scripts that import this helper live under blog/scripts/ or
  // blog/scripts/lib/. Resolve relative to the helper itself.
  const blogDir = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
  const repoRoot = join(blogDir, '..');
  const source = join(repoRoot, sourceRel);
  const dest = join(blogDir, destRel);
  return { here, blogDir, repoRoot, source, dest };
}

/**
 * Wipe every entry in `dest` whose filename matches one of the given
 * extensions (e.g. ['.md', '.json']). Recursive subdirectories are also
 * removed so the destination mirrors the latest source layout.
 */
export async function clearDest(dest, extensions) {
  if (!existsSync(dest)) return;
  for (const entry of await readdir(dest, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      await rm(join(dest, entry.name), { recursive: true, force: true });
      continue;
    }
    if (extensions.some((ext) => entry.name.endsWith(ext))) {
      await rm(join(dest, entry.name));
    }
  }
}

/**
 * Read the YAML frontmatter block from a markdown file as a flat
 * string->string mapping. Quoted scalars are unwrapped. Sequences and
 * nested objects are not supported — callers that need richer parsing
 * should validate downstream with Zod after the sync.
 */
export function readFrontmatter(filePath) {
  const text = readFileSync(filePath, 'utf-8');
  if (!text.startsWith('---\n')) return null;
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return null;
  const block = text.slice(4, end);
  const body = text.slice(end + 5);
  const data = {};
  for (const line of block.split('\n')) {
    const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$/);
    if (!match) continue;
    let value = match[2].trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1).replace(/\\"/g, '"');
    }
    data[match[1]] = value;
  }
  return { data, body };
}

/**
 * Run a sync function with a uniform error envelope. On any thrown
 * error, log a tagged message and exit with status 1 so the build fails
 * instead of silently shipping a partial content collection.
 */
export async function runSync(tag, fn) {
  try {
    await fn();
  } catch (err) {
    const message = err && err.stack ? err.stack : String(err);
    console.error(`[${tag}] sync failed: ${message}`);
    process.exit(1);
  }
}

/**
 * Copy a single file, surfacing the source path in any error so the
 * operator can find the offending document immediately.
 */
export async function copyOne(from, to) {
  try {
    await copyFile(from, to);
  } catch (err) {
    throw new Error(`failed to copy ${from} -> ${to}: ${err.message}`);
  }
}

/**
 * Convenience: ensure a destination directory exists.
 */
export async function ensureDir(path) {
  await mkdir(path, { recursive: true });
}
