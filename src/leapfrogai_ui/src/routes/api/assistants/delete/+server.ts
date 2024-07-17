import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import { stringIdSchema } from '$schemas/chat';

export const DELETE: RequestHandler = async ({ request, locals: { supabase, session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { id: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await stringIdSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const openai = getOpenAiClient(session.access_token);
  const assistantDeleted = await openai.beta.assistants.del(requestData.id);
  if (!assistantDeleted.deleted) {
    console.error(`error deleting assistant: ${JSON.stringify(assistantDeleted)}`);
    error(500, 'Error deleting assistant');
  }

  const { error: supabaseError } = await supabase.storage
    .from('assistant_avatars')
    .remove([requestData.id]);
  if (supabaseError) {
    // fail silently
    console.error(
      `Error deleting assistant avatar. AssistantId: ${requestData.id}, error: ${error}`
    );
  }

  return new Response(undefined, { status: 204 });
};
