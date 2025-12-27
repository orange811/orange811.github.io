import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
    site: 'https://piyush-jain.me',
    output: 'static',
    integrations: [tailwind()],
});
