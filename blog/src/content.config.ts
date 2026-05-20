import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Published posts. Drafts (`draft: true`) may omit `abstract` so a
// Fellow can stage work-in-progress; anything visible on the site
// (`draft: false`) must ship with one. The conditional requirement is
// applied with `superRefine` instead of `z.discriminatedUnion` because
// posts omit the `draft` field entirely (relying on the default), and
// the discriminator runs before defaults in this version of Zod.
//
// Tags remain optional in both states: the institute's current
// pipeline does not emit them, and a `min(1)` invariant would block
// every publication today.
const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z
    .object({
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
    })
    .superRefine((data, ctx) => {
      if (!data.draft && (!data.abstract || data.abstract.trim() === '')) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ['abstract'],
          message: 'Published posts (draft: false) must define a non-empty abstract.',
        });
      }
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
//
// The enum here is a deliberately wider superset of what the sync
// script copies in. The sync's PUBLIC_KINDS filter decides which kinds
// reach the blog; the schema accepts any value the institute can
// legitimately write so a kind added to the orchestrator never crashes
// the build before the sync filter has a chance to drop it.
const decisions = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/decisions' }),
  schema: z.object({
    kind: z.enum([
      'admission',
      'advisor_review',
      'andon_cord_outcome',
      'andon_cord_pulled',
      'bootstrap',
      'charter_violation_termination',
      'concern',
      'curriculum_response',
      'editorial',
      'editorial_ruling',
      'final_revision_required',
      'kill_switch',
      'needs_assessment',
      'peer_review',
      'policy_change',
      'preprint_comment',
      'preprint_posted',
      'promotion',
      'promotion_review',
      'proposal',
      'proposal_review',
      'publication',
      'qualifying_panel',
      'qualifying_proposal',
      'reading_group',
      'recovery',
      'release',
      'research',
      'retirement',
      'revision',
      'revision_required',
      'rollback',
      'senior_fellow_confirmed',
      'step_failure',
    ]),
    recorded_at: z.coerce.date(),
    actors: z.array(z.string()).default([]),
    project: z.string().optional(),
  }),
});

// Corrections (Chapter 8). Each correction names the post it amends,
// what changed, and why. Surfaced both on the corrected post and on
// the standalone /corrections page accessible from the site footer.
const corrections = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/corrections' }),
  schema: z.object({
    postSlug: z.string(),
    issuedAt: z.coerce.date(),
    summary: z.string(),
    severity: z
      .enum(['typo', 'clarification', 'factual', 'retraction'])
      .default('factual'),
  }),
});

// Working preprints. Each entry is a single version of an in-flight
// project; ids have the shape `<projectId>--v<N>`. Synced from
// archive/preprints/<projectId>/v<N>.md by scripts/sync-preprints.mjs.
const preprints = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/preprints' }),
  schema: z.object({
    title: z.string(),
    projectId: z.string(),
    lead: z.string(),
    leadId: z.string(),
    version: z.coerce.number().int().min(1),
    postedAt: z.coerce.date(),
    projectStateAtPost: z.string(),
    abstract: z.string().min(1),
  }),
});

export const collections = {
  posts,
  notebooks,
  reviews,
  fellows,
  decisions,
  corrections,
  preprints,
};
