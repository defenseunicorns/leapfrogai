import type { Actions } from './$types';
import { redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

// TODO - test keycloak full logout with e2e
export const actions: Actions = {
  signout: async ({ locals: { supabase, safeGetSession }, cookies }) => {
    const { session } = await safeGetSession();
    if (session) {
      const url = new URL(
        `${env.SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL}/protocol/openid-connect/logout`
      );

      if (session.provider_refresh_token) {
        // Append query parameters
        const params = new URLSearchParams();
        params.append('client_id', env.SUPABASE_AUTH_KEYCLOAK_CLIENT_ID);
        params.append('client_secret', env.SUPABASE_AUTH_KEYCLOAK_SECRET);
        params.append('refresh_token', session.provider_refresh_token!);

        const res = await fetch(
          `${env.SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL}/protocol/openid-connect/logout`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params
          }
        );
        if (res.status !== 204) {
          console.error('Failed to logout from Keycloak', res.status, res.statusText);
        }
      }

      await supabase.auth.signOut();
      throw redirect(303, '/');
    }
  }
};
