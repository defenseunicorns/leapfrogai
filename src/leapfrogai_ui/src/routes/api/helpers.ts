import type { LFThread } from '$lib/types/threads';
import { getOpenAiClient } from '$lib/server/constants';
import type { LFMessage } from '$lib/types/messages';

export const getThreadWithMessages = async (
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
