import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { optimizeCss } from 'carbon-preprocess-svelte';

export default defineConfig(() => ({
  plugins: [sveltekit(), optimizeCss()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest-setup.ts'],
    include: ['src/**/*.{test,spec}.{js,ts}'],
    globals: true
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData:
          '@use "@carbon/themes/scss/themes" as *; @use "@carbon/themes" with ($theme: $g90); @use "@carbon/layout"; @use "@carbon/type"; @use "@carbon/colors" as *;'
      }
    }
  }
}));
