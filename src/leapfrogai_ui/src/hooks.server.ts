import { createServerClient } from '@supabase/ssr';
import { type Handle, redirect } from '@sveltejs/kit';
import { sequence } from '@sveltejs/kit/hooks';
import { env } from '$env/dynamic/public';
import { env as envPrivate } from '$env/dynamic/private';

const supabase: Handle = async ({ event, resolve }) => {
  /**
   * Creates a Supabase client specific to this server request.
   *
   * The Supabase client gets the Auth token from the request cookies.
   */
  event.locals.supabase = createServerClient(
    env.PUBLIC_SUPABASE_URL,
    env.PUBLIC_SUPABASE_ANON_KEY,
    {
      cookies: {
        getAll: () => event.cookies.getAll(),
        /**
         * SvelteKit's cookies API requires `path` to be explicitly set in
         * the cookie options. Setting `path` to `/` replicates previous/
         * standard behavior.
         */
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => {
            event.cookies.set(name, value, { ...options, path: '/' });
          });
        }
      }
    }
  );

  /**
   * Unlike `supabase.auth.getSession()`, which returns the session _without_
   * validating the JWT, this function also calls `getUser()` to validate the
   * JWT before returning the session.
   */
  event.locals.safeGetSession = async () => {
    const {
      data: { session }
    } = await event.locals.supabase.auth.getSession();
    if (!session) {
      return { session: null, user: null };
    }

    const {
      data: { user },
      error
    } = await event.locals.supabase.auth.getUser();
    if (error) {
      // JWT validation has failed
      return { session: null, user: null };
    }

    return { session, user };
  };

  return resolve(event, {
    filterSerializedResponseHeaders(name) {
      /**
       * Supabase libraries use the `content-range` and `x-supabase-api-version`
       * headers, so we need to tell SvelteKit to pass it through.
       */
      return name === 'content-range' || name === 'x-supabase-api-version';
    }
  });
};

const authGuard: Handle = async ({ event, resolve }) => {
  const { session, user } = await event.locals.safeGetSession();
  event.locals.session = session;
  event.locals.user = user;
  event.locals.isUsingOpenAI = !!envPrivate.OPENAI_API_KEY;

  // protect all routes under /chat
  if (!event.locals.session && event.url.pathname.startsWith('/chat')) {
    redirect(303, '/');
  }

  // if already authenticated, redirect to /chat
  if (event.locals.session && event.url.pathname === '/') {
    redirect(303, '/chat');
  }

  return resolve(event);
};

const csp: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);
  const directives = {
    'default-src': ["'none'"],
    'base-uri': ["'self'"],
    'object-src': ["'none'"], // typically used for legacy content, such as Flash files or Java applets
    'style-src': ["'self'", "'unsafe-inline'"],
    'font-src': ["'self'"],
    'manifest-src': ["'self'"],
    'img-src': ["'self'", `data: 'self'  ${process.env.PUBLIC_SUPABASE_URL}`, `blob: 'self'`],
    'media-src': ["'self'"],
    'form-action': ["'self'"],
    'connect-src': [
      "'self'",
      process.env.LEAPFROGAI_API_BASE_URL,
      process.env.PUBLIC_SUPABASE_URL,
      process.env.SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL,
      `wss://${process.env.PUBLIC_SUPABASE_URL!.replace('https://', '')}` // supabase realtime websocket
    ],
    'child-src': ["'none'"],
    'frame-src': [`blob: 'self'`],
    'frame-ancestors': ["'none'"]
  };

  const CSP = Object.entries(directives)
    .map(([key, arr]) => key + ' ' + arr.join(' '))
    .join('; ');
  // We use Sveltekits generated CSP for script-src to get the nonce
  const svelteKitGeneratedCSPWithNonce = response.headers.get('Content-Security-Policy');
  response.headers.set('Content-Security-Policy', `${CSP}; ${svelteKitGeneratedCSPWithNonce}`);
  return response;
};

export const handle: Handle = sequence(csp, supabase, authGuard);
