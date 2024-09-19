import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { handleError } from '$helpers/apiHelpers';
import { getOpenAiClient } from '$lib/server/constants';

export const POST: RequestHandler = async ({ params, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  if (!params?.thread_id || !params?.message_id) {
    error(400, 'Bad Request');
  }

  try {
    const openai = getOpenAiClient(session.access_token);
    const message = await openai.beta.threads.messages.update(params.thread_id, params.message_id, {

    });
  } catch (e) {
    return handleError(e);
  }
};
