import { error, json } from '@sveltejs/kit';
import { newThreadInputSchema } from '$lib/schemas/chat';
import type { Profile } from '$lib/types/profile';
import { openai } from '$lib/server/constants';

export async function POST({ request, locals: { supabase, getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  // Validate request body
  let requestData: { label: string };
  try {
    requestData = await request.json();
    const isValid = await newThreadInputSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const newThread = await openai.beta.threads.create({
    metadata: { user_id: session.user.id, label: requestData.label }
  });

  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', session.user.id)
    .returns<Profile[]>()
    .single();

  if (profileError) {
    console.log(
      `Error getting user profile while creating thread: ${JSON.stringify(profileError)}`
    );
    error(500, 'Error creating thread');
  }

  const { error: supabaseError } = await supabase
    .from('profiles')
    .update({ thread_ids: [...profile?.thread_ids, newThread.id] })
    .eq('id', session.user.id);

  if (supabaseError) {
    console.log(`Error creating thread in supabase: ${JSON.stringify(supabaseError)}`);
    error(500, 'Error creating thread');
  }

  return json(newThread);
}
