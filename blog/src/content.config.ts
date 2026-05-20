import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    issueNumber: z.number().int().positive().optional(),
    authors: z.array(z.string()).min(1),
    publishedAt: z.coerce.date(),
    revisedAt: z.coerce.date().optional(),
    reviewers: z.array(z.string()).optional(),
    abstract: z.string().optional(),
    tags: z.array(z.string()).optional(),
    projectId: z.string().optional(),
    hasNotebook: z.boolean().default(false),
    hasReviews: z.boolean().default(false),
    draft: z.boolean().default(false),
  }),
});

// A research project's lab notebook. Append-only public log of the actual
// research process: dead ends, dated entries, decisions, corrections.
// Slug matches the publication slug it belongs to.
const notebooks = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/notebooks' }),
  schema: z.object({
    title: z.string(),
    postSlug: z.string(),
    projectId: z.string(),
    authors: z.array(z.string()).min(1),
    startedAt: z.coerce.date(),
    completedAt: z.coerce.date().optional(),
  }),
});

// A signed peer review. One review per reviewer per piece. Reviews are public.
// Slug format: <post-slug>--<reviewer-id>.
const reviews = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/reviews' }),
  schema: z.object({
    title: z.string(),
    postSlug: z.string(),
    reviewer: z.string(),
    submittedAt: z.coerce.date(),
    recommendation: z.enum(['accept', 'minor', 'major', 'reject']),
    confidence: z.enum(['confident', 'moderate', 'low']),
    role: z.enum(['primary', 'secondary', 'outside']),
    dissent: z.boolean().default(false),
    round: z.number().int().min(1).default(1),
  }),
});

// Fellow genomes live at the repo root in genomes/. A presync script
// (`scripts/sync-fellows.mjs`, run by `npm run dev` / `npm run build`)
// copies them into this content collection directory because Astro's
// glob loader does not reach outside the project root.
const fellows = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/fellows' }),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    rank: z.enum([
      'postulant',
      'novice',
      'junior_fellow',
      'fellow',
      'senior_fellow',
      'emeritus',
    ]),
    model: z.string(),
    specialization: z.string(),
    system_prompt_addendum: z.string(),
    allowed_tools: z.array(z.string()).default([]),
    behavioral_notes: z.record(z.string(), z.string()).default({}),
    advisor_id: z.string().nullable().optional(),
    current_research: z.string().nullable().optional(),
  }),
});

// Institutional decision records: admissions, promotions, releases,
// editorial rulings, andon-cord pulls. Synced from archive/decisions/
// at build time by scripts/sync-decisions.mjs. Filtered to the kinds
// that belong on the public /records page.
const decisions = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/decisions' }),
  schema: z.object({
    kind: z.string(),
    recorded_at: z.coerce.date(),
    actors: z.array(z.string()).default([]),
    project: z.string().optional(),
  }),
});

export const collections = { posts, notebooks, reviews, fellows, decisions };
