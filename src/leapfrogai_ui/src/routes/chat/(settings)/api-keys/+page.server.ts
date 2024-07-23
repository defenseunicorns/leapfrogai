import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { newAPIKeySchema } from '$schemas/apiKey';
import { type APIKeyRow } from '$lib/types/apiKeys';
import { env } from '$env/dynamic/private';

export const load = async ({ depends, locals: { safeGetSession } }) => {
  depends('lf:api-keys');
  const form = await superValidate(yup(newAPIKeySchema));

  const { session } = await safeGetSession();
  if (!session) {
    error(401, { message: 'Unauthorized' });
  }

  // Feature Flag - if using OpenAI, disable API Keys page
  if (env.OPENAI_API_KEY) {
    throw redirect(303, '/');
  }

  let keys: APIKeyRow[] = [];

  const res = await fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/api-keys`, {
    headers: {
      Authorization: `Bearer ${session.access_token}`
    }
  });

  if (!res.ok) {
    return error(500, { message: 'Error fetching API keys' });
  }

  keys = await res.json();
  // convert from seconds to milliseconds
  keys.forEach((key) => {
    key.created_at = key.created_at * 1000;
    key.expires_at = key.expires_at * 1000;
  });

  return { title: 'LeapfrogAI - API Keys', form, keys };
};

export const actions = {
  default: async ({ request, locals: { safeGetSession } }) => {
    const { session } = await safeGetSession();
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    const form = await superValidate(request, yup(newAPIKeySchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    const res = await fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/api-keys`, {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(form.data)
    });
    if (!res.ok) {
      return fail(500, { form });
    }
    const newKey = await res.json();

    return {
      form,
      key: newKey
    };
  }
};
