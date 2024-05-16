import { error } from '@sveltejs/kit';
import { deleteMessageSchema } from '$lib/schemas/chat';
import OpenAI from 'openai';
import { env } from '$env/dynamic/private';

const openai = new OpenAI({
  apiKey: env.LEAPFROGAI_API_KEY ?? '',
  baseURL: env.LEAPFROGAI_API_BASE_URL
});

export async function DELETE({ request, locals: { getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { thread_id: string; message_id: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await deleteMessageSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const response = await openai.beta.threads.messages.del(
    requestData.thread_id,
    requestData.message_id
  );

  if (!response.deleted) {
    console.log(`error deleting message: ${response}`);
    error(500, 'Error deleting message');
  }

  return new Response(undefined, { status: 204 });
}
