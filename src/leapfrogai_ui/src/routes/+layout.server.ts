import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals: { session, isUsingOpenAI }, cookies }) => {
  return {
    session,
    cookies: cookies.getAll(),
    isUsingOpenAI
  };
};
