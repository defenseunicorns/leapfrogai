import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors
  preprocess: [vitePreprocess()],
  compilerOptions: {
    customElement: true
  },
  kit: {
    // adapter-auto only supports some environments, see https://kit.svelte.dev/docs/adapter-auto for a list.
    // If your environment is not supported or you settled on a specific environment, switch out the adapter.
    // See https://kit.svelte.dev/docs/adapters for more information about adapters.
    adapter: adapter(),
    alias: {
      $components: 'src/lib/components',
      $webComponents: 'src/lib/web-components',
      $stores: 'src/lib/stores',
      $helpers: 'src/lib/helpers',
      $assets: 'src/lib/assets',
      $schemas: 'src/lib/schemas',
      $constants: 'src/lib/constants',
      $testUtils: 'testUtils'
    }
  }
};

export default config;
