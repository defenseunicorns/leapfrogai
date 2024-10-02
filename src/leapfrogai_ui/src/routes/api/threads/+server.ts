import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import type { Profile } from '$lib/types/profile';
import type { LFThread } from '$lib/types/threads';
import { getThreadWithMessages } from '../helpers';

export const GET: RequestHandler = async ({ locals: { session, supabase, user } }) => {
  if (!session) {
    error(401, 'Unauthorized');
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
    error(500, 'Internal Error');
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
      return json([]);
    }
  }

  return json(threads);
};
