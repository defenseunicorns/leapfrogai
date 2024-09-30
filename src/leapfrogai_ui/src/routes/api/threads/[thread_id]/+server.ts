import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import { getThreadWithMessages } from '../../helpers';

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
