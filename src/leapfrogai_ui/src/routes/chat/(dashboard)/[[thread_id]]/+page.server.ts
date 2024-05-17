import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import OpenAI from 'openai';
import { env } from '$env/dynamic/private';

const openai = new OpenAI({
  apiKey: env.LEAPFROGAI_API_KEY ?? '',
  baseURL: env.LEAPFROGAI_API_BASE_URL
});

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
    console.log(
      `error getting user profile for user_id: ${session.user.id}. ${JSON.stringify(profileError)}`
    );
    throw redirect(303, '/');
  }

  const threads: LFThread[] = [];
  for (const thread_id of profile.thread_ids) {
    const thread = await openai.beta.threads.retrieve(thread_id);
    const messagesPage = await openai.beta.threads.messages.list(thread.id);
    const messages = messagesPage.data;
    messages.sort((a, b) => a.created_at - b.created_at);
    threads.push({ ...thread, messages: messages });
  }

  return { title: 'LeapfrogAI - Chat', session, profile, threads };
};
