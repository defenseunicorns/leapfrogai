import OpenAI from 'openai';
import {
	PUBLIC_DEFAULT_MODEL,
	PUBLIC_DEFAULT_SYSTEM_PROMPT,
	PUBLIC_DEFAULT_TEMPERATURE,
	PUBLIC_LEAPFROGAI_API_BASE_URL
} from '$env/static/public';
import { env } from '$env/dynamic/private';
import { OpenAIStream, StreamingTextResponse } from 'ai';
import { messagesSchema } from '../../../schemas/chat';
import { error } from '@sveltejs/kit';

// Set the runtime to edge for best performance
export const config = {
	runtime: 'edge'
};

// This endpoint is called by the Vercel AI SDK handleSubmit function
export async function POST({ request }) {

	const openai = new OpenAI({
		apiKey: env.LEAPFROGAI_API_KEY,
		baseURL: PUBLIC_LEAPFROGAI_API_BASE_URL
	});

	let messages: AIMessage[];

	try {
		const body = await request.json();
		messages = body.messages;
	} catch (e) {
		error(400, { message: 'Bad Request' });
	}
	if (!messages) error(400, { message: 'Bad Request' });

	const validMessages = await messagesSchema.isValid(messages);

	if (!validMessages) error(400, { message: 'Bad Request' });

	// Add the default system prompt to the beginning of the messages
	messages.unshift({ content: PUBLIC_DEFAULT_SYSTEM_PROMPT, role: 'system' });

	const response = await openai.chat.completions.create({
		model: PUBLIC_DEFAULT_MODEL,
		temperature: Number(PUBLIC_DEFAULT_TEMPERATURE),
		max_tokens: 1000,
		stream: true,
		messages: messages
	});

	const stream = OpenAIStream(response);
	return new StreamingTextResponse(stream);
}
