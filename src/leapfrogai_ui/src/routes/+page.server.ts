import type { PageServerLoad } from './$types';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { emailPasswordSchema } from '$schemas/auth';

export const load: PageServerLoad = async ({ url }) => {
  const form = await superValidate(yup(emailPasswordSchema));

  return { url: url.origin, form };
};
