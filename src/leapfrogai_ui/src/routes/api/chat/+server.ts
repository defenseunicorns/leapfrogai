import { StreamingTextResponse, streamText } from 'ai';
import { createOpenAI } from '@ai-sdk/openai';
import { env } from '$env/dynamic/private';
import { error } from '@sveltejs/kit';
import { getMessageText } from '$helpers/threads';
import type { LFMessage } from '$lib/types/messages';
import { AIMessagesInputSchema } from '$schemas/messageSchema';

export async function POST({ request, locals: { safeGetSession } }) {
  const { session } = await safeGetSession();

  if (!session) {
    error(401, 'Unauthorized');
  }

  let messages;
  // Validate request body
  try {
    const requestBody = await request.json();
    const isValid = await AIMessagesInputSchema.isValid(requestBody);
    if (!isValid) error(400, 'Bad Request');
    messages = requestBody.messages;
  } catch {
    error(400, 'Bad Request');
  }
  const openai = createOpenAI({
    apiKey: env.OPENAI_API_KEY ? env.OPENAI_API_KEY : session.access_token,
    baseURL: env.LEAPFROGAI_API_BASE_URL
  });

  // Add the default system prompt to the beginning of the messages
  if (messages[0].content !== env.DEFAULT_SYSTEM_PROMPT) {
    messages.unshift({ content: env.DEFAULT_SYSTEM_PROMPT!, role: 'system' });
  }

  const reformatedMessages = messages.map((message: LFMessage) => ({
    ...message,
    content: getMessageText(message)
  }));

  const result = await streamText({
    model: openai(env.DEFAULT_MODEL),
    messages: reformatedMessages
  });

  return new StreamingTextResponse(result.toAIStream());
}
