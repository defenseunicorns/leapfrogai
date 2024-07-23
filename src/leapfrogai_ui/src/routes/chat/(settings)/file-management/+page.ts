import type { PageLoad } from './$types';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';

export const load: PageLoad = async () => {
  const form = await superValidate(yup(filesSchema));

  return { title: 'LeapfrogAI - File Management', form };
};
