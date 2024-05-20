import { error, json } from '@sveltejs/kit';
import { object, string } from 'yup';
import { openai } from '$lib/server/constants';

export async function DELETE({ request, locals: { supabase, getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { id: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await object({ id: string().required() }).isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  try {
    const response = await openai.beta.assistants.del(requestData.id);

    const { error } = await supabase.storage.from('assistant_avatars').remove([requestData.id]);
    if (error) {
      // fail silently
      console.log(
        `Error deleting assistant avatar. AssistantId: ${requestData.id}, error: ${error}`
      );
    }

    return json(response);
  } catch (e) {
    console.log(`Error deleting assistant: ${e}`);
    error(500, 'Error deleting assistant');
  }
}
