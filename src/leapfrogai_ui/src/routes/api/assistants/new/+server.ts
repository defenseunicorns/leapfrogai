import { error, json } from '@sveltejs/kit';
import { supabaseAssistantInputSchema } from '../../../../schemas/assistants';
import { assistantDefaults } from '$lib/constants';
import { env } from '$env/dynamic/private';

export async function POST({ request, locals: { supabase, getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: NewAssistantInput;

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await supabaseAssistantInputSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const assistant: Omit<Assistant, 'id' | 'created_at'> = {
    ...assistantDefaults,
    ...requestData,
    model: env.DEFAULT_MODEL,
    metadata: {
      ...assistantDefaults.metadata,
      ...requestData.metadata,
      created_by: session.user.id
    }
  };

  const { error: responseError, data: createdAssistant } = await supabase
    .from('assistants')
    .insert(assistant)
    .select()
    .returns<Assistant[]>();

  if (responseError) {
    console.log(
      `error creating assistant,  error status: ${responseError.code}: ${responseError.message}`
    );
    error(500, { message: 'Internal Server Error' });
  }

  return json(createdAssistant[0]);
}
