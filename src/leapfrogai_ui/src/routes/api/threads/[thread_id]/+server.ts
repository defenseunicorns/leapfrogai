import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import type { LFThread } from '$lib/types/threads';
import type { LFMessage } from '$lib/types/messages';

const getThreadWithMessages = async (
  thread_id: string,
  access_token: string
): Promise<LFThread | null> => {
  const openai = getOpenAiClient(access_token);
  const thread = (await openai.beta.threads.retrieve(thread_id)) as LFThread;
  if (!thread) {
    return null;
  }
  const messagesPage = await openai.beta.threads.messages.list(thread.id);

  const messages = messagesPage.data as LFMessage[];
  messages.sort((a, b) => a.created_at - b.created_at);
  return { ...thread, messages: messages };
};

export const GET: RequestHandler = async ({ params, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  if (!params?.thread_id) error(400, 'Bad Request');

  try {
    const thread = await getThreadWithMessages(params.thread_id, session.access_token);
    return json(thread);
  } catch (e) {
    console.error(`Error getting thread: ${e}`);
    error(500, 'Error getting thread');
  }
};
