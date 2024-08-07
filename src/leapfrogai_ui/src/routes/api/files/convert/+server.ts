import { error } from '@sveltejs/kit';
import { promisify } from 'util';
import libre from 'libreoffice-convert';
import { stringIdSchema } from '$schemas/chat';
import { getOpenAiClient } from '$lib/server/constants';
import type { RequestHandler } from './$types';

// Note - this throws a warning, but it seems erroneous as libre.convert does not return a promise and this is
// IAW with the documentation:
// (node:18447) [DEP0174] DeprecationWarning: Calling promisify on a function that returns a Promise is likely a mistake.
const convertAsync = promisify(libre.convert);

/**
 * Converts a file to PDF.
 */
export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { id: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await stringIdSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const openai = getOpenAiClient(session.access_token);
  const fileMetadata = await openai.files.retrieve(requestData.id);
  const fileRes = await openai.files.content(requestData.id);

  const file = await fileRes.arrayBuffer();

  if (file || fileMetadata) {
    try {
      const ext = '.pdf';
      let pdfBuf = await convertAsync(Buffer.from(file), ext, undefined);
      return new Response(pdfBuf, {
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': `attachment; filename="${fileMetadata.filename}${ext}"`
        }
      });
    } catch (e) {
      console.error('file conversion error', e);
      error(500, 'Internal Error');
    }
  } else error(404, 'File Not Found');
};