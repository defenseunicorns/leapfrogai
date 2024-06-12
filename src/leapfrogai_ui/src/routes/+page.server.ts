import { redirect } from '@sveltejs/kit';

export const load = async ({ url, locals: { safeGetSession } }) => {
  const { session } = await safeGetSession();

  // if the user is already logged in return them to the chat page
  if (session) {
    throw redirect(303, '/chat');
  }

  return { url: url.origin };
};
