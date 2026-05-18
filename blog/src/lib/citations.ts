/**
 * Build a bidirectional citation graph from the posts collection.
 *
 * Every post body may contain markdown links to other posts in the
 * College. We walk each post's rendered/raw markdown looking for links
 * that match the internal post URL pattern, and build a map of
 * postSlug -> array of slugs that cite it.
 *
 * Used by the post page to render a "Cited by" block in the Apparatus
 * footer, surfacing the reverse-citation relationships across the
 * Archive as the body of work grows.
 */

import type { CollectionEntry } from 'astro:content';

type Post = CollectionEntry<'posts'>;

// Matches any markdown link whose target looks like a College post link:
//   posts/<slug>            (relative form recommended in the brief)
//   /the-invisible-college/posts/<slug>   (absolute with base path)
//   posts/<slug>/           (with trailing slash)
const LINK_RE =
  /\[[^\]]+\]\((?:\/the-invisible-college\/)?posts\/([A-Za-z0-9_-]+)\/?\)/g;

export function citingSlugsFor(
  body: string,
  knownSlugs: Set<string>,
): string[] {
  const out = new Set<string>();
  for (const match of body.matchAll(LINK_RE)) {
    const slug = match[1];
    if (knownSlugs.has(slug)) {
      out.add(slug);
    }
  }
  return [...out];
}

/**
 * Compute, for every post, the list of OTHER posts that cite it.
 * Returns a map keyed by cited-post slug; the value is the list of citing
 * posts (newest first).
 */
export function buildBacklinkMap(posts: Post[]): Map<string, Post[]> {
  const knownSlugs = new Set(posts.map((p) => p.id));
  const backlinks = new Map<string, Post[]>();

  for (const post of posts) {
    const cited = citingSlugsFor(post.body ?? '', knownSlugs);
    for (const target of cited) {
      if (target === post.id) continue; // ignore self-links
      const arr = backlinks.get(target) ?? [];
      arr.push(post);
      backlinks.set(target, arr);
    }
  }

  for (const [slug, arr] of backlinks) {
    arr.sort(
      (a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime(),
    );
    backlinks.set(slug, arr);
  }

  return backlinks;
}
