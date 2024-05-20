import OpenAI from 'openai';
import { env } from '$env/dynamic/private';
import { OpenAIStream, StreamingTextResponse } from 'ai';
import type { ChatCompletionMessageParam } from 'ai/prompts';
import { messagesInputSchema } from '$lib/schemas/chat';
import { error } from '@sveltejs/kit';

// Set the runtime to edge for best performance
export const config = {
  runtime: 'edge'
};

// This endpoint is called by the Vercel AI SDK handleSubmit function
export async function POST({ request, locals: { getSession } }) {
  const session = await getSession();
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { messages: ChatCompletionMessageParam[] };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await messagesInputSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const openai = new OpenAI({
    apiKey: env.LEAPFROGAI_API_KEY,
    baseURL: env.LEAPFROGAI_API_BASE_URL
  });

  // Add the default system prompt to the beginning of the messages
  if (requestData.messages[0].content !== env.DEFAULT_SYSTEM_PROMPT) {
    requestData.messages.unshift({ content: env.DEFAULT_SYSTEM_PROMPT!, role: 'system' });
  }

  const response = await openai.chat.completions.create({
    model: env.DEFAULT_MODEL!,
    temperature: Number(env.DEFAULT_TEMPERATURE!),
    max_tokens: 1000,
    stream: true,
    messages: requestData.messages
  });

  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
