import { error, json } from '@sveltejs/kit';
import { openai } from '$lib/server/constants';

export async function GET({ url, locals: { safeGetSession } }) {
  const { session } = await safeGetSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  const thread_id = url.searchParams.get('thread_id');
  const message_id = url.searchParams.get('message_id');

  if (!message_id || !thread_id) error(400, 'Invalid request');
  try {
    const message = await openai.beta.threads.messages.retrieve(thread_id, message_id);
    return json(message);
  } catch (e) {
    console.error(`Error getting message: ${e}`);
    error(500, 'Error getting message');
  }
}
