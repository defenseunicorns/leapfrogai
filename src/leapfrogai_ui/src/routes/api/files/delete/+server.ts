import { error } from '@sveltejs/kit';
import { openai } from '$lib/server/constants';
import { stringIdArraySchema } from '$schemas/chat';

export async function DELETE({ request, locals: { getSession } }) {
  const session = await getSession();
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
    let fileDeleted: any;
    try {
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
}
