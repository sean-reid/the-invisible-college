import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
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
  }),
});

export const collections = { posts, notebooks, reviews };
