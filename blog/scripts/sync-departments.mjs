#!/usr/bin/env node
/**
 * Copy archive/departments/*.md from the repo root into the Astro
 * content collection directory before each build/dev run.
 *
 * The institute writes departments as one markdown file per open
 * department. The body of each file is the human-written description;
 * chair, members, and dates live in the YAML frontmatter so the page
 * can render proper Astro links with the GitHub Pages base URL.
 *
 * Validation: this script checks required frontmatter fields and exits
 * non-zero on the first broken file. The Zod schema in
 * src/content.config.ts re-validates at build time; this pre-check
 * just gives the operator a clearer error than the Astro type-generator
 * would.
 */

import { existsSync } from 'node:fs';
import { readdir, copyFile } from 'node:fs/promises';
import { join } from 'node:path';
import {
  clearDest,
  ensureDir,
  readFrontmatter,
  resolvePaths,
  runSync,
} from './lib/sync.mjs';

const TAG = 'sync-departments';

const REQUIRED_FIELDS = ['id', 'name', 'created_at'];

await runSync(TAG, async () => {
  const { source, dest } = resolvePaths(
    import.meta.url,
    'archive/departments',
    'src/content/departments',
  );

  await ensureDir(dest);
  await clearDest(dest, ['.md']);

  if (!existsSync(source)) {
    console.log(`[${TAG}] no source directory at ${source}; nothing to copy`);
    return;
  }

  let copied = 0;
  for (const file of await readdir(source)) {
    if (!file.endsWith('.md')) continue;
    const srcPath = join(source, file);
    const fm = readFrontmatter(srcPath);
    if (!fm) {
      throw new Error(`${srcPath} has no parseable YAML frontmatter`);
    }
    for (const field of REQUIRED_FIELDS) {
      if (!(field in fm.data) || fm.data[field] === '') {
        throw new Error(`${srcPath} is missing required field '${field}'`);
      }
    }
    // The id in frontmatter must match the filename slug; otherwise the
    // page routing silently breaks.
    const expectedSlug = file.replace(/\.md$/, '');
    if (fm.data.id !== expectedSlug) {
      throw new Error(
        `${srcPath} frontmatter id='${fm.data.id}' does not match filename '${expectedSlug}'`,
      );
    }
    await copyFile(srcPath, join(dest, file));
    copied += 1;
  }
  console.log(`[${TAG}] copied ${copied} department(s) to ${dest}`);
});
