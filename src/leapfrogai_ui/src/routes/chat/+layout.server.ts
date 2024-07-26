import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import type { LFMessage } from '$lib/types/messages';
import { getOpenAiClient } from '$lib/server/constants';

/**
 * This file is necessary to ensure protection of all routes in the `chat`
 * directory. It makes the routes in this directory _dynamic_ routes, which
 * send a server request, and thus trigger `hooks.server.ts`.
 * Keep it even if there is no code in it.
 **/

const getThreadWithMessages = async (
  thread_id: string,
  access_token: string
): Promise<LFThread | null> => {
  try {
    const openai = getOpenAiClient(access_token);
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

export const load: LayoutServerLoad = async ({ locals: { supabase, session, user } }) => {
  if (!session) {
    throw redirect(303, '/');
  }

  const { data: profile, error: profileError } = await supabase
    .from('profiles')
    .select(`*`)
    .eq('id', user?.id)
    .returns<Profile[]>()
    .single();

  if (profileError) {
    console.error(
      `error getting user profile for user_id: ${user?.id}. ${JSON.stringify(profileError)}`
    );
    throw redirect(303, '/');
  }

  const threads: LFThread[] = [];
  if (profile?.thread_ids && profile?.thread_ids.length > 0) {
    try {
      const threadPromises = profile.thread_ids.map((thread_id) =>
        getThreadWithMessages(thread_id, session.access_token)
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

  return { threads };
};
