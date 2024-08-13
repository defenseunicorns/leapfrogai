import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import * as dotenv from 'dotenv';

dotenv.config();
/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors
  preprocess: [vitePreprocess()],
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
    },
    csp: {
      directives: {
        'default-src': ['none'],
        'base-uri': ['self'],
        'script-src': ['self', 'strict-dynamic'],
        'object-src': ['none'], // typically used for legacy content, such as Flash files or Java applets
        'style-src': ['self', 'unsafe-inline'],
        'font-src': ['self'],
        'manifest-src': ['self'],
        'img-src': [
          'self',
          `data: ${process.env.ORIGIN} ${process.env.PUBLIC_SUPABASE_URL}`,
          `blob: ${process.env.ORIGIN}`
        ],
        'media-src': ['self'],
        'form-action': ['self'],
        'connect-src': [
          'self',
          process.env.LEAPFROGAI_API_BASE_URL || '',
          process.env.PUBLIC_SUPABASE_URL || '',
          process.env.SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL || ''
        ],
        'child-src': ['none'], // note - this will break the annotations story and will need to updated to allow the correct resource
        'frame-ancestors': ['none']
      }
    }
  }
};

export default config;
