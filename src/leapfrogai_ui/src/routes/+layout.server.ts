import type { LayoutServerLoad } from './$types';
import { env } from '$env/dynamic/private';

export const load = (async ({ locals: { safeGetSession } }) => {
  const { session, user } = await safeGetSession();

  return {
    session,
    user,
    isUsingOpenAI: !!env.OPENAI_API_KEY
  };
}) satisfies LayoutServerLoad;
