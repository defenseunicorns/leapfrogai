import type { LFAssistant } from '$lib/types/assistants';
import type { LFThread } from '$lib/types/threads';
import type { LFMessage } from '$lib/types/messages';

export const load = async ({ fetch, params, depends }) => {
  depends('ai:thread');
  const response = await fetch('/api/assistants');
  const assistants = (await response.json()) as LFAssistant[];

  const [threadResponse, messagesResponse] = await Promise.all([
    fetch(`/api/threads/${params.thread_id}`),
    fetch(`/api/messages/${params.thread_id}`)
  ]);
  const thread = (await threadResponse.json()) as LFThread;
  const messages = (await messagesResponse.json()) as LFMessage[];

  return { title: 'LeapfrogAI - Assistants', assistants: assistants ?? [], thread, messages };
};
