// Build-time enumeration of code/data artifacts for a published post.
// Files live under blog/public/code/<project_id>/ after `institute
// publish` mirrors them out of archive/code/. We list them here so the
// post template can render a "Code & data" row in the apparatus.

import { existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

// Single source of truth for the blog package root. Astro's content
// pipeline runs with cwd set to the blog/ directory; resolve all
// build-time file lookups against this constant so every helper in
// lib/ agrees on the same anchor.
export const REPO_ROOT = process.cwd();

export type Artifact = {
  name: string;
  size: number;
  ext: string;
};

export function listArtifacts(projectId: string): Artifact[] {
  const dir = join(REPO_ROOT, 'public', 'code', projectId);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((name) => !name.startsWith('.'))
    .map((name) => {
      const full = join(dir, name);
      const st = statSync(full);
      if (!st.isFile()) return null;
      const dot = name.lastIndexOf('.');
      const ext = dot >= 0 ? name.slice(dot + 1).toLowerCase() : '';
      return { name, size: st.size, ext };
    })
    .filter((a): a is Artifact => a !== null)
    .sort((a, b) => a.name.localeCompare(b.name));
}

export function humanSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
