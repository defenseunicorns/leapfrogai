import { error, json } from '@sveltejs/kit';
import { updateThreadLabelSchema } from '$lib/schemas/chat';
import { openai } from '$lib/server/constants';

export async function PUT({ request, locals: { safeGetSession } }) {
  const { session } = await safeGetSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { id: string; label: string };
  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await updateThreadLabelSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  try {
    const updatedThread = await openai.beta.threads.update(requestData.id, {
      metadata: { label: requestData.label }
    });
    return json(updatedThread);
  } catch (e) {
    console.error(`Error updating thread label: ${e}`);
    error(500, 'Error updating thread label');
  }
}
