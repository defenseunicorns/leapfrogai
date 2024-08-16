import { error } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import type { RequestHandler } from './$types';
import { convertFileToPdf } from './utils';

/**
 * Converts a file to PDF.
 */
export const GET: RequestHandler = async ({ params, request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  const { id } = params;
  if (!id || typeof id !== 'string') error(400, 'Bad Request');

  const openai = getOpenAiClient(session.access_token);
  const fileMetadata = await openai.files.retrieve(id);
  if (!fileMetadata) error(404, 'File Not Found');
  let fileRes: Response;
  let fileArrayBuffer: ArrayBuffer;
  try {
    fileRes = await openai.files.content(id);
    fileArrayBuffer = await fileRes.arrayBuffer();
  } catch (e) {
    console.error(`Error getting file content for file ${JSON.stringify(fileMetadata)}: `, e);
    error(500, 'Internal Error');
  }
  if (!fileArrayBuffer) error(404, 'File Not Found');
  try {
    return await convertFileToPdf(fileArrayBuffer, fileMetadata.filename);
  } catch (e) {
    console.error('file conversion error', e);
    error(500, 'Internal Error');
  }
};
