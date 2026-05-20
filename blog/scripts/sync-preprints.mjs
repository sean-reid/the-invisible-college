#!/usr/bin/env node
/**
 * Copy archive/preprints/<project_id>/v<N>.md from the repo root into
 * the Astro content collection directory before each build/dev run.
 *
 * The institute writes preprints as one markdown file per version,
 * nested under a per-project directory. The blog flattens that layout
 * into a single content collection: each entry id is
 * `<project_id>--v<N>` so Astro's `getCollection` returns versions as
 * independent records that the preprint pages can group by project.
 *
 * Validation: this script does a quick required-field check on the
 * frontmatter and exits non-zero on the first broken file. The Zod
 * schema in src/content.config.ts re-validates at build time; this
 * pre-check just gives the operator a clearer error than the Astro
 * type-generator would.
 */

import { existsSync, statSync } from 'node:fs';
import { readdir, writeFile, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import {
  clearDest,
  ensureDir,
  readFrontmatter,
  resolvePaths,
  runSync,
} from './lib/sync.mjs';

const TAG = 'sync-preprints';

const REQUIRED_FIELDS = [
  'title',
  'projectId',
  'lead',
  'leadId',
  'version',
  'postedAt',
  'projectStateAtPost',
  'abstract',
];

await runSync(TAG, async () => {
  const { source, dest } = resolvePaths(
    import.meta.url,
    'archive/preprints',
    'src/content/preprints',
  );

  await ensureDir(dest);
  await clearDest(dest, ['.md']);

  if (!existsSync(source)) {
    console.log(`[${TAG}] no source directory at ${source}; nothing to copy`);
    return;
  }

  let copied = 0;
  for (const projectEntry of await readdir(source)) {
    const projectDir = join(source, projectEntry);
    let st;
    try {
      st = statSync(projectDir);
    } catch (err) {
      throw new Error(`stat failed for ${projectDir}: ${err.message}`);
    }
    if (!st.isDirectory()) continue;

    for (const file of await readdir(projectDir)) {
      const match = file.match(/^v(\d+)\.md$/);
      if (!match) continue;
      const version = parseInt(match[1], 10);
      const srcPath = join(projectDir, file);
      const fm = readFrontmatter(srcPath);
      if (!fm) {
        throw new Error(`${srcPath} has no parseable YAML frontmatter`);
      }
      for (const field of REQUIRED_FIELDS) {
        if (!(field in fm.data) || fm.data[field] === '') {
          throw new Error(`${srcPath} is missing required field '${field}'`);
        }
      }
      // projectId in frontmatter must agree with the directory name —
      // otherwise routing by id silently breaks.
      if (fm.data.projectId !== projectEntry) {
        throw new Error(
          `${srcPath} frontmatter projectId='${fm.data.projectId}' does not match ` +
            `directory '${projectEntry}'`,
        );
      }
      if (Number(fm.data.version) !== version) {
        throw new Error(
          `${srcPath} frontmatter version='${fm.data.version}' does not match ` +
            `filename v${version}`,
        );
      }
      const destName = `${projectEntry}--v${version}.md`;
      const text = await readFile(srcPath, 'utf-8');
      await writeFile(join(dest, destName), text);
      copied += 1;
    }
  }
  console.log(`[${TAG}] copied ${copied} preprint version(s) to ${dest}`);
});
