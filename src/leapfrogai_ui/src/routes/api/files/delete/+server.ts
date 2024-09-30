import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import { stringIdArraySchema } from '$schemas/chat';

export const DELETE: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }
  let requestData: { ids: string[] };
  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await stringIdArraySchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  for (const id of requestData.ids) {
    let fileDeleted;
    try {
      const openai = getOpenAiClient(session.access_token);

      fileDeleted = await openai.files.del(id);
      if (!fileDeleted.deleted) {
        console.error(`Unable to delete file: ${JSON.stringify(fileDeleted)}`);
        error(500, 'Unable to delete file');
      }
    } catch (e) {
      console.error(`Unable to delete file: ${e}`);
      error(500, 'Unable to delete file');
    }
  }

  return new Response(undefined, { status: 204 });
};
