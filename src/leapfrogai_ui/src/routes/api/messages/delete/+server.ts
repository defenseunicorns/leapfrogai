import { error } from '@sveltejs/kit';
import { deleteMessageSchema } from '$lib/schemas/chat';
import { openai } from '$lib/server/constants';

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

  const messageDeleted = await openai.beta.threads.messages.del(
    requestData.thread_id,
    requestData.message_id
  );

  if (!messageDeleted.deleted) {
    console.error(`error deleting message: ${JSON.stringify(messageDeleted)}`);
    error(500, 'Error deleting message');
  }

  return new Response(undefined, { status: 204 });
}
