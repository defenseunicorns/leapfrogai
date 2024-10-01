import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { stringIdArraySchema } from '$schemas/chat';
import { env } from '$env/dynamic/private';

/**
 * Handles the DELETE request to revoke one or more API keys.
 */
export const DELETE: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }
  let requestData: { ids: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await stringIdArraySchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const promises: Promise<Response>[] = [];
  for (const id of requestData.ids) {
    promises.push(
      fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/api-keys/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${session.access_token}`,
          'Content-Type': 'application/json'
        }
      })
    );
  }
  const results = await Promise.allSettled(promises);
  results.forEach((result) => {
    if (
      result.status === 'rejected' ||
      !(result.value.status === 200 || result.value.status === 204)
    ) {
      const msg = `Error deleting API ${requestData.ids.length > 1 ? 'keys' : 'key'}`;
      console.error(`${msg} ${JSON.stringify(result)}`);
      error(500, msg);
    }
  });
  return new Response(undefined, { status: 204 });
};
