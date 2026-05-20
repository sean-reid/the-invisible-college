import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { remarkNormalizePostLinks } from './src/remark/normalize-post-links.mjs';

const BASE = '/the-invisible-college';

export default defineConfig({
  site: 'https://sean-reid.github.io',
  base: BASE,
  trailingSlash: 'never',
  integrations: [mdx(), sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    shikiConfig: {
      theme: 'github-light',
      wrap: true,
    },
    // remark-math parses $...$ inline and $$...$$ display math in the
    // markdown AST. rehype-katex turns those nodes into KaTeX HTML at
    // build time. KaTeX CSS is imported globally via Base.astro so
    // the rendered math picks up the proper typography.
    remarkPlugins: [
      [remarkNormalizePostLinks, { base: BASE }],
      remarkMath,
    ],
    rehypePlugins: [rehypeKatex],
  },
});
