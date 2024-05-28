import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import { openai } from '$lib/server/constants';
import type { LFMessage } from '$lib/types/messages';

export const load: PageServerLoad = async ({ locals: { supabase, getSession } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', session.user.id)
    .returns<Profile[]>()
    .single();

  if (profileError) {
    console.error(
      `error getting user profile for user_id: ${session.user.id}. ${JSON.stringify(profileError)}`
    );
    throw redirect(303, '/');
  }

  const threads: LFThread[] = [];
  if (profile?.thread_ids && profile?.thread_ids.length > 0) {
    for (const thread_id of profile.thread_ids) {
      try {
        const thread = (await openai.beta.threads.retrieve(thread_id)) as LFThread;
        const messagesPage = await openai.beta.threads.messages.list(thread.id);
        const messages = messagesPage.data as LFMessage[];
        messages.sort((a, b) => a.created_at - b.created_at);
        threads.push({ ...thread, messages: messages });
      } catch {
        // fail silently
      }
    }
  }

  return { title: 'LeapfrogAI - Chat', session, profile, threads };
};
