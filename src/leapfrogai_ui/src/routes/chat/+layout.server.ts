import { redirect } from '@sveltejs/kit';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import { openai } from '$lib/server/constants';
import type { LFMessage } from '$lib/types/messages';

export const load = async ({ locals: { supabase, safeGetSession } }) => {
  const { session } = await safeGetSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', session.user?.id)
    .returns<Profile[]>()
    .single();

  if (profileError) {
    console.error(
      `error getting user profile for user_id: ${session.user?.id}. ${JSON.stringify(profileError)}`
    );
    throw redirect(303, '/');
  }

  const threads: LFThread[] = [];
  if (profile?.thread_ids && profile?.thread_ids.length > 0) {
    try {
      const threadPromises = profile.thread_ids.map(async (thread_id) => {
        const thread = (await openai.beta.threads.retrieve(thread_id)) as LFThread;
        const messagesPage = await openai.beta.threads.messages.list(thread.id);
        const messages = messagesPage.data as LFMessage[];
        messages.sort((a, b) => a.created_at - b.created_at);
        return { ...thread, messages: messages };
      });

      const resolvedThreads = await Promise.all(threadPromises);
      threads.push(...resolvedThreads);
    } catch (e) {
      console.error(`Error fetching thread: ${e}`);
      // fail silently
      return null;
    }
  }

  return { title: 'LeapfrogAI - Chat', session, profile, threads };
};
