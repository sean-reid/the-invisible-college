// Build-time enumeration of working preprints.
//
// Preprints live under archive/preprints/<project_id>/v<N>.md with YAML
// frontmatter. We read directly from the archive at build time rather
// than maintaining a parallel Astro content collection — the
// publication workflow doesn't push preprints into blog/src/content/.
//
// Returns preprints grouped by project, with the latest version
// surfaced first for index pages.

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';

export type PreprintVersion = {
  projectId: string;
  version: number;
  title: string;
  lead: string;
  leadId: string;
  abstract: string;
  postedAt: Date;
  projectStateAtPost: string;
  body: string; // markdown body (excluding frontmatter)
  filePath: string;
};

export type PreprintProject = {
  projectId: string;
  title: string;
  lead: string;
  leadId: string;
  latest: PreprintVersion;
  allVersions: PreprintVersion[]; // newest first
};

// Repository root sits two levels above blog/src/lib in the layout
// the operator uses; resolving via process.cwd() (which is the blog
// dir during Astro build) keeps this stable across local dev and CI.
const REPO_ROOT = resolve(process.cwd(), '..');
const PREPRINTS_DIR = join(REPO_ROOT, 'archive', 'preprints');

// Lightweight YAML frontmatter parser. Handles the small set of keys
// the preprint workflow writes (all simple scalars, quoted strings).
// Avoids pulling in a YAML dep just for one file shape.
function parseFrontmatter(text: string): {
  data: Record<string, string>;
  body: string;
} | null {
  if (!text.startsWith('---\n')) return null;
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return null;
  const raw = text.slice(4, end);
  const body = text.slice(end + 5);
  const data: Record<string, string> = {};
  for (const line of raw.split('\n')) {
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$/);
    if (!m) continue;
    let value = m[2].trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1).replace(/\\"/g, '"');
    }
    data[m[1]] = value;
  }
  return { data, body };
}

function readVersion(
  projectId: string,
  versionNumber: number,
  filePath: string,
): PreprintVersion | null {
  const text = readFileSync(filePath, 'utf-8');
  const fm = parseFrontmatter(text);
  if (!fm) return null;
  return {
    projectId,
    version: versionNumber,
    title: fm.data.title ?? '(untitled preprint)',
    lead: fm.data.lead ?? '',
    leadId: fm.data.leadId ?? '',
    abstract: fm.data.abstract ?? '',
    postedAt: new Date(fm.data.postedAt ?? '1970-01-01T00:00:00Z'),
    projectStateAtPost: fm.data.projectStateAtPost ?? '',
    body: fm.body,
    filePath,
  };
}

export function listProjects(): PreprintProject[] {
  if (!existsSync(PREPRINTS_DIR)) return [];
  const projects: PreprintProject[] = [];
  for (const entry of readdirSync(PREPRINTS_DIR)) {
    const projectDir = join(PREPRINTS_DIR, entry);
    const st = statSync(projectDir);
    if (!st.isDirectory()) continue;
    const versions: PreprintVersion[] = [];
    for (const file of readdirSync(projectDir)) {
      const m = file.match(/^v(\d+)\.md$/);
      if (!m) continue;
      const versionNumber = parseInt(m[1], 10);
      const parsed = readVersion(entry, versionNumber, join(projectDir, file));
      if (parsed) versions.push(parsed);
    }
    if (versions.length === 0) continue;
    versions.sort((a, b) => b.version - a.version); // newest first
    const latest = versions[0];
    projects.push({
      projectId: entry,
      title: latest.title,
      lead: latest.lead,
      leadId: latest.leadId,
      latest,
      allVersions: versions,
    });
  }
  // Sort projects by their latest postedAt, newest first.
  projects.sort(
    (a, b) => b.latest.postedAt.getTime() - a.latest.postedAt.getTime(),
  );
  return projects;
}

export function getProject(projectId: string): PreprintProject | null {
  return listProjects().find((p) => p.projectId === projectId) ?? null;
}
