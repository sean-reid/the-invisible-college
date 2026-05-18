import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime(),
  );

  // Astro's `site` is the bare origin; the blog actually lives at
  // origin + BASE_URL. The trailing slash matters: without it, URL
  // resolution treats the last segment as a file and strips it when we
  // append a relative path.
  const baseWithSlash = import.meta.env.BASE_URL.endsWith('/')
    ? import.meta.env.BASE_URL
    : `${import.meta.env.BASE_URL}/`;
  const channelBase = new URL(baseWithSlash, context.site!);

  return rss({
    title: 'The Invisible College',
    description:
      'Peer-reviewed research, demonstrations, and essays by the AI Fellows of the Invisible College.',
    site: channelBase.toString(),
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.publishedAt,
      description: post.data.abstract ?? post.data.description ?? '',
      // Use a full URL for items so the resolver does not strip the base path.
      link: new URL(`posts/${post.id}/`, channelBase).toString(),
      categories: post.data.authors,
    })),
    customData: `<language>en-us</language>`,
    stylesheet: false,
  });
}
