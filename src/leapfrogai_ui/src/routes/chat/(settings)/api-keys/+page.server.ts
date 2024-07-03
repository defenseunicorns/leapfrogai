import { message, superValidate, fail as superformsFail } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { newAPIKeySchema } from '$schemas/apiKey';
import { type APIKeyRow, PERMISSIONS } from '$lib/types/apiKeys';
import { error, fail, redirect } from '@sveltejs/kit';
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

  // const res = await fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/list-api-keys`, {
  //   headers: {
  //     Authorization: `Bearer ${session.access_token}`
  //   }
  // });
  //
  // if (!res.ok) {
  //   return error(500, { message: 'Error fetching API keys' });
  // }
  //
  // keys = await res.json();

  keys = [
    {
      id: '1',
      name: 'key-1',
      api_key: 'lfai_fghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expires_at: new Date().getTime(),
      permissions: PERMISSIONS.ALL
    },
    {
      id: '2',
      name: 'key-2',
      api_key: 'lfai_fghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expires_at: new Date().getTime(),
      permissions: PERMISSIONS.WRITE
    },
    {
      id: '3',
      name: 'key-3',
      api_key: 'lfai_fghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expires_at: new Date().getTime(),
      permissions: PERMISSIONS.READ_WRITE
    },
    {
      id: '4',
      name: 'key-4',
      api_key: 'lfai_fghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expires_at: new Date().getTime(),
      permissions: PERMISSIONS.READ
    }
  ];
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
      return superformsFail(400, { form });
    }

    // const res = await fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/create-api-key`, {
    //   headers: { Authorization: `Bearer ${session.access_token}` },
    //   method: 'POST',
    //   body: JSON.stringify(form.data)
    // });
    // if (!res.ok) {
    //   throw new Error('Error creating API key');
    // }
    return { form, key: '123451234512345' }; // TODO - replace with response from API
  }
};
