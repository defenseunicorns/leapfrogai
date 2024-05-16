import { createOpenAI } from '@ai-sdk/openai';
import { StreamingTextResponse, streamText } from 'ai';
import type { Message as AIMessage } from 'ai';
import type { RequestHandler } from './$types';

import { env } from '$env/dynamic/private';
import { error } from '@sveltejs/kit';
import { getMessageText } from '$helpers/threads';
import type { LFMessage } from '$lib/types/messages';

const openai = createOpenAI({
  apiKey: env.LEAPFROGAI_API_KEY ?? '',
  baseURL: env.LEAPFROGAI_API_BASE_URL
});

export const POST = (async ({ request, locals: { getSession } }) => {
  const session = await getSession();

  if (!session) {
    error(401, 'Unauthorized');
  }

  const { messages } = await request.json();

  // Add the default system prompt to the beginning of the messages
  if (messages[0].content !== env.DEFAULT_SYSTEM_PROMPT) {
    messages.unshift({ content: env.DEFAULT_SYSTEM_PROMPT!, role: 'system' });
  }

  const reformatedMessages = messages.map((message: LFMessage) => ({
    ...message,
    content: getMessageText(message)
  }));

  const result = await streamText({
    model: openai('gpt-4-turbo-preview'),
    messages: reformatedMessages
  });

  return new StreamingTextResponse(result.toAIStream());
}) satisfies RequestHandler;
