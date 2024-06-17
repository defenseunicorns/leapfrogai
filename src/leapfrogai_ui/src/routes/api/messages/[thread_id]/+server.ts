import { error, json } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';

export async function GET({ params, locals: { safeGetSession } }) {
  const { session } = await safeGetSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  if (!params.thread_id) error(400, 'Invalid request');
  try {
    const openai = getOpenAiClient(session.access_token);
    const threadMessages = await openai.beta.threads.messages.list(params.thread_id);
    return json(threadMessages.data);
  } catch (e) {
    console.error(`Error getting messages: ${e}`);
    error(500, 'Error getting messages');
  }
}
