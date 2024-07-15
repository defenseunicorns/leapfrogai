import { error } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';

export async function GET({ params, locals: { safeGetSession } }) {
  const { session } = await safeGetSession();
  if (!session) {
    error(401, 'Unauthorized');
  }
  try {
    const file_id = params.file_id;
    if (!file_id) error(400, 'Bad Request');
    const openai = getOpenAiClient(session.access_token);
    const res = await openai.files.content(params.file_id);
    return new Response(res.body, {
      headers: {
        'Content-Type': res.headers.get('content-type') || 'application/json'
      }
    });
  } catch (e) {
    console.error(`Error getting file: ${e}`);
    error(500, 'Error getting file');
  }
}
