import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig(() => ({
	plugins: [sveltekit()],
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
					'@use "@carbon/themes/scss/themes" as *; @use "@carbon/themes" with ($theme: $g90); @use "@carbon/layout"; @use "@carbon/type";'
			}
		}
	}
}));
