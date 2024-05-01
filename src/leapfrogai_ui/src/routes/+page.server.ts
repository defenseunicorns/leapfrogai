import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ url, locals: { getSession } }) => {
  const session = await getSession();

  // if the user is already logged in return them to the chat page
  if (session) {
    throw redirect(303, '/chat');
  }

  return { url: url.origin };
};
