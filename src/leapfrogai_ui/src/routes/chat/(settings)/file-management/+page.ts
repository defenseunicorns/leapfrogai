import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';
import type { FileObject } from 'openai/resources/files';

export const load = async ({ fetch, depends }) => {
  depends('lf:files');
  const filesRes = await fetch('/api/files');
  const files = (await filesRes.json()) as FileObject[];

  const form = await superValidate(yup(filesSchema));

  return { title: 'LeapfrogAI - File Management', form, files };
};
