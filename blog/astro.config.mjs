import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
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
    remarkPlugins: [[remarkNormalizePostLinks, { base: BASE }]],
  },
});
