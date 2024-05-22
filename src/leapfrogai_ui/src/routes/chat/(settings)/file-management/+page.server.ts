import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import { openai } from '$lib/server/constants';

export const load: PageServerLoad = async ({ locals: { getSession } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const list = await openai.files.list();
  console.log(list.data);

  return { title: 'LeapfrogAI - File Management', files: list.data };
};
