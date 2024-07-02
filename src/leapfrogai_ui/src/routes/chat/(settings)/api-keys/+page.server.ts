import { message, superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { newAPIKeySchema } from '$schemas/apiKey';
import { type APIKeyRow, PERMISSIONS } from '$lib/types/apiKeys';
import { fail } from '@sveltejs/kit';

export const load = async ({ depends }) => {
  depends('lf:api-keys');
  const form = await superValidate(yup(newAPIKeySchema));

  let keys: APIKeyRow[] = [
    {
      id: '1',
      name: 'key-1',
      key: 'abcdefghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expiration: new Date().getTime(),
      permissions: PERMISSIONS.ALL
    },
    {
      id: '2',
      name: 'key-2',
      key: 'abcdefghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expiration: new Date().getTime(),
      permissions: PERMISSIONS.WRITE
    },
    {
      id: '3',
      name: 'key-3',
      key: 'abcdefghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expiration: new Date().getTime(),
      permissions: PERMISSIONS.READ_WRITE
    },
    {
      id: '4',
      name: 'key-4',
      key: 'abcdefghijklmnopqrstuvwxyz',
      created_at: new Date().getTime(),
      expiration: new Date().getTime(),
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
      return fail(400, { form });
    }

    // TODO - create API key call here
    console.log('form submission data', form.data);

    return message(form, 'API key created');
  }
};
