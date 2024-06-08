import { redirect } from '@sveltejs/kit';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import { openai } from '$lib/server/constants';
import type { LFMessage } from '$lib/types/messages';

const getThreadWithMessages = async (thread_id: string): Promise<LFThread | null> => {
  try {
    const thread = (await openai.beta.threads.retrieve(thread_id)) as LFThread;
    if (!thread) {
      return null;
    }
    const messagesPage = await openai.beta.threads.messages.list(thread.id);
    const messages = messagesPage.data as LFMessage[];
    messages.sort((a, b) => a.created_at - b.created_at);
    return { ...thread, messages: messages };
  } catch (e) {
    console.error(`Error fetching thread or messages: ${e}`);
    return null;
  }
};

export const load = async ({ fetch, locals: { supabase, safeGetSession } }) => {
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
      const threadPromises = profile.thread_ids.map((thread_id) =>
        getThreadWithMessages(thread_id)
      );
      const results = await Promise.allSettled(threadPromises);

      results.forEach((result) => {
        if (result.status === 'fulfilled' && result.value) {
          threads.push(result.value);
        }
      });
    } catch (e) {
      console.error(`Error fetching threads: ${e}`);
      // fail silently
      return null;
    }
  }

  const promises = [fetch('/api/assistants'), fetch('/api/files')];
  const [assistantsRes, filesRes] = await Promise.all(promises);

  const assistants = await assistantsRes.json();
  const files = await filesRes.json();

  return { threads, assistants, files };
};
