import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import { messageInputSchema } from '$lib/schemas/chat';
import type { NewMessageInput } from '$lib/types/messages';
import { getOpenAiClient } from '$lib/server/constants';
import { ValidationError } from 'yup';

export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    return error(401, 'Unauthorized');
  }

  let requestData: NewMessageInput;

  // Validate request body
  try {
    requestData = (await request.json()) as NewMessageInput;
    if (requestData.lengthOverride) {
      await messageInputSchema.validate(requestData, { abortEarly: false });
    } else {
      await messageInputSchema.validate(requestData, { abortEarly: false });
    }
    delete requestData.lengthOverride;
  } catch (validationError) {
    if (validationError instanceof ValidationError) {
      console.log('Validation error:', validationError.errors);
      return error(400, `Bad Request: ${validationError.errors.join(', ')}`);
    }
    return error(400, 'Bad Request');
  }

  try {
    const openai = getOpenAiClient(session.access_token);

    const threadMessages = await openai.beta.threads.messages.create(requestData.thread_id, {
      role: requestData.role,
      content: requestData.content,
      metadata: requestData.metadata || null
    });
    return json(threadMessages);
  } catch (e) {
    console.error(`Error creating message: ${e}`);
    error(500, 'Error creating message');
  }
};
