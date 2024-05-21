import { error, json } from '@sveltejs/kit';
import { openai } from '$lib/server/constants';

export async function GET({ request, params, locals: { getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  try {
    const thread = await openai.beta.threads.retrieve(params.thread_id);
    return json(thread);
  } catch (e) {
    console.error(`Error getting thread: ${e}`);
    error(500, 'Error getting thread');
  }
}
