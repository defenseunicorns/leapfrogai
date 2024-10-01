import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

/**
 * This file is necessary to ensure protection of all routes in the `chat`
 * directory. It makes the routes in this directory _dynamic_ routes, which
 * send a server request, and thus trigger `hooks.server.ts`.
 * Keep it even if there is no code in it.
 **/

export const load: LayoutServerLoad = async ({ locals: { session, isUsingOpenAI } }) => {
  if (!session) {
    throw redirect(303, '/');
  }

  return { isUsingOpenAI };
};
