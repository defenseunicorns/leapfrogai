import { env } from '$env/dynamic/public';
import type { LayoutLoad } from './$types';
import { createBrowserClient, isBrowser, parse } from '@supabase/ssr';

export const load = (async ({ fetch, data, depends }) => {
  depends('supabase:auth');

  const supabase = createBrowserClient(env.PUBLIC_SUPABASE_URL, env.PUBLIC_SUPABASE_ANON_KEY, {
    global: {
      fetch
    },
    cookies: {
      get(key) {
        if (!isBrowser()) {
          return JSON.stringify(data.session);
        }

        const cookie = parse(document.cookie);
        return cookie[key];
      }
    }
  });

  /**
   * It's fine to use `getSession` here, because on the client, `getSession` is
   * safe, and on the server, it reads `session` from the `LayoutData`, which
   * safely checked the session using `safeGetSession`.
   */
  const {
    data: { session }
  } = await supabase.auth.getSession();

  return { supabase, session };
}) satisfies LayoutLoad;
