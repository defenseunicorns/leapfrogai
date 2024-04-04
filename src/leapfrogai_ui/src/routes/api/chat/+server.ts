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
export async function POST({ request, locals: { getSession } }) {
	const session = await getSession();
	if (!session) {
		error(401, 'Unauthorized');
	}

	let requestData: { messages: AIMessage[] };

	// Validate request body
	try {
		requestData = await request.json();
		const isValid = await messagesSchema.isValid(requestData);
		if (!isValid) error(400, 'Bad Request');
	} catch {
		error(400, 'Bad Request');
	}

	const openai = new OpenAI({
		apiKey: env.LEAPFROGAI_API_KEY,
		baseURL: PUBLIC_LEAPFROGAI_API_BASE_URL
	});

	// Add the default system prompt to the beginning of the messages
	if (requestData.messages[0].content !== PUBLIC_DEFAULT_SYSTEM_PROMPT) {
		requestData.messages.unshift({ content: PUBLIC_DEFAULT_SYSTEM_PROMPT, role: 'system' });
	}

	const response = await openai.chat.completions.create({
		model: PUBLIC_DEFAULT_MODEL,
		temperature: Number(PUBLIC_DEFAULT_TEMPERATURE),
		max_tokens: 1000,
		stream: true,
		messages: requestData.messages
	});

	const stream = OpenAIStream(response);
	return new StreamingTextResponse(stream);
}
