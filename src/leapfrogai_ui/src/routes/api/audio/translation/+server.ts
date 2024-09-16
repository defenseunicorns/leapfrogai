import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getOpenAiClient } from '$lib/server/constants';
import { audioFileSchema } from '$schemas/files';
import { env } from '$env/dynamic/private';

export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let file: File | null;

  // Validate request body
  try {
    const formData = await request.formData();
    file = formData.get('file') as File;

    await audioFileSchema.validate({ file }, { abortEarly: false });
  } catch (e) {
    console.error('Validation error:', e);
    error(400, `Bad Request, File invalid: ${e}`);
  }

  try {
    const openai = getOpenAiClient(session.access_token);
    const translation = await openai.audio.translations.create({
      file: file,
      model: env.OPENAI_API_KEY ? 'whisper-1' : 'whisper'
    });
    return json({ text: translation.text });
  } catch (e) {
    console.error('file translation error', e);
    error(500, 'Internal Error');
  }
};
