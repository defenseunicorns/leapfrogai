import { error } from '@sveltejs/kit';
import type { Profile } from '$lib/types/profile';
import { openai } from '$lib/server/constants';
import { stringIdSchema } from '$schemas/chat';

export async function DELETE({ request, locals: { supabase, getSession } }) {
  const session = await getSession();
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

  const threadDeleted = await openai.beta.threads.del(requestData.id);

  if (!threadDeleted.deleted) {
    console.error(`Unable to delete thread: ${JSON.stringify(threadDeleted)}`);
    error(500, 'Unable to delete thread');
  }

  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', session.user.id)
    .returns<Profile[]>()
    .single();
  if (profileError) {
    console.error(
      `Error getting user profile while deleting thread: ${JSON.stringify(profileError)}`
    );
    error(500, 'Error deleting thread');
  }

  const updatedThreadIds = profile?.thread_ids.filter((id) => id !== requestData.id);

  const { error: supabaseError } = await supabase
    .from('profiles')
    .update({ thread_ids: updatedThreadIds })
    .eq('id', session.user.id);

  if (supabaseError) {
    console.error(`Error deleting thread in supabase: ${JSON.stringify(supabaseError)}`);
    error(500, 'Error deleting thread');
  }
  return new Response(undefined, { status: 204 });
}
