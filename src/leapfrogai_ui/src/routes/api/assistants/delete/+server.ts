import { error } from '@sveltejs/kit';
import { uuidSchema } from '../../../../schemas/chat';

export async function DELETE({ request, locals: { supabase, getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { id: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await uuidSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const { error: responseError } = await supabase
    .from('assistants')
    .delete()
    .eq('id', requestData.id);

  if (responseError) {
    console.log(
      `error deleting assistant, error status: ${responseError?.code}: ${responseError?.message}`
    );
    error(500, 'Error deleting assistant');
  }

  return new Response(undefined, { status: 204 });
}
