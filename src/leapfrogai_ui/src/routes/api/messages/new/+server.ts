import { error, json } from '@sveltejs/kit';
import { messageInputSchema } from '$lib/schemas/chat';
import OpenAI from 'openai';
import { env } from '$env/dynamic/private';
import type { NewMessageInput } from '$lib/types/messages';

const openai = new OpenAI({
  apiKey: env.LEAPFROGAI_API_KEY ?? '',
  baseURL: env.LEAPFROGAI_API_BASE_URL
});

export async function POST({ request, locals: { getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: NewMessageInput;

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await messageInputSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const threadMessages = await openai.beta.threads.messages.create(requestData.thread_id, {
    role: requestData.role,
    content: requestData.content
  });

  return json(threadMessages);
}
