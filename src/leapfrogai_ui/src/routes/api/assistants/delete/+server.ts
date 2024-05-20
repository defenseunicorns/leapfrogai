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

  const response = await openai.beta.assistants.del(requestData.id);

  return json(response);
}
