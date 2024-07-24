import type { LayoutServerLoad } from './$types';
import { env } from '$env/dynamic/private';

export const load: LayoutServerLoad = async ({ locals: { session }, cookies }) => {
  return {
    session,
    cookies: cookies.getAll(),
    isUsingOpenAI: !!env.OPENAI_API_KEY
  };
};
