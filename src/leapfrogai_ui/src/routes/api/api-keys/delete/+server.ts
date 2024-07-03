import { error } from '@sveltejs/kit';
import { stringIdArraySchema } from '$schemas/chat';
import { env } from '$env/dynamic/private';

/**
 * Handles the DELETE request to revoke one or more API keys.
 */
export async function DELETE({ request, locals: { safeGetSession } }) {
  const { session } = await safeGetSession();
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
      fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/revoke-api-key`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${session.access_token}` },
        body: JSON.stringify({ id })
      })
    );
  }

  await Promise.all(promises);
  // TODO - handle error

  // const res = await fetch(`${env.LEAPFROGAI_API_BASE_URL}/leapfrogai/v1/auth/revoke-api-key`, {
  //   method: 'DELETE',
  //   headers: { Authorization: `Bearer ${session.access_token}` },
  //   body: JSON.stringify({ ids: requestData.ids })
  // });
  // if (!res.ok) {
  //   console.error(`error revoking API key(s): ${res.status}`);
  //   error(500, 'Error revoking API key(s)');
  // }
  return new Response(undefined, { status: 204 });
}
