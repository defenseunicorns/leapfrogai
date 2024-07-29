import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { setError, superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { emailPasswordSchema } from '$schemas/auth';

export const actions: Actions = {
  signup: async ({ request, locals: { supabase } }) => {
    const form = await superValidate(request, yup(emailPasswordSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    const email = form.data.email;
    const password = form.data.password;

    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      if (error.code === 'user_already_exists') {
        console.log('user already exists');
        return setError(form, 'email', 'User already exists');
      }
      console.error(error);
      return setError(form, 'email', 'Unknown error');
    } else {
      redirect(303, '/chat');
    }
  },
  login: async ({ request, locals: { supabase } }) => {
    const form = await superValidate(request, yup(emailPasswordSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    const email = form.data.email;
    const password = form.data.password;

    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      console.error(error);
      return setError(form, 'email', 'Login error');
    } else {
      redirect(303, '/chat');
    }
  },
  signout: async ({ locals: { supabase, session } }) => {
    if (session) {
      if (session.provider_refresh_token) {
        const params = new URLSearchParams();
        params.append('client_id', env.SUPABASE_AUTH_KEYCLOAK_CLIENT_ID);
        params.append('client_secret', env.SUPABASE_AUTH_KEYCLOAK_SECRET);
        params.append('refresh_token', session.provider_refresh_token!);

        console.log("refresh token", session.provider_refresh_token);
        console.log("req url", `${env.SUPABASE_AUTH_EXTERNAL_KEYCLOAK_URL}/protocol/openid-connect/logout`);
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
