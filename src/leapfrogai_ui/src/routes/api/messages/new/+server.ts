import { error, json } from '@sveltejs/kit';
import { messageInputSchema } from '$lib/schemas/chat';
import type { NewMessageInput } from '$lib/types/messages';
import { openai } from '$lib/server/constants';

export async function POST({ request, locals: { safeGetSession } }) {
  const { session } = await safeGetSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: NewMessageInput;

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await messageInputSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch(e) {
    error(400, 'Bad Request');
  }

  try {
    const threadMessages = await openai.beta.threads.messages.create(requestData.thread_id, {
      role: requestData.role,
      content: requestData.content
    });
    return json(threadMessages);
  } catch (e) {
    console.error(`Error creating message: ${e}`);
    error(500, 'Error creating message');
  }
}
