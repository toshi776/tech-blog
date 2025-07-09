import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://toshi776.com',
  base: '/blog',
  output: 'static',
  integrations: [mdx(), sitemap()],
});