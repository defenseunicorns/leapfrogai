import { error } from '@sveltejs/kit';
import OpenAI from 'openai';
import { env } from '$env/dynamic/private';
import { string } from 'yup';
import type { Profile } from '$lib/types/profile';

const openai = new OpenAI({
  apiKey: env.LEAPFROGAI_API_KEY ?? '',
  baseURL: env.LEAPFROGAI_API_BASE_URL
});

export async function DELETE({ request, locals: { supabase, getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { id: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await string().required().isValid(requestData.id);

    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const response = await openai.beta.threads.del(requestData.id);

  if (!response.deleted) {
    console.log(`error deleting thread: ${response}`);
    error(500, 'Error deleting thread');
  }

  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', session.user.id)
    .returns<Profile[]>()
    .single();
  if (profileError) {
    console.log(
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
    console.log(`Error deleting thread in supabase: ${JSON.stringify(supabaseError)}`);
    error(500, 'Error deleting thread');
  }
  return new Response(undefined, { status: 204 });
}
