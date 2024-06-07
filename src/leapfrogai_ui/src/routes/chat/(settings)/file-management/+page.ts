import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';

export const load = async ({ fetch }) => {
  const response = await fetch('/api/files');
  const files = await response.json();
  const form = await superValidate(yup(filesSchema));

  return { title: 'LeapfrogAI - File Management', files, form };
};
