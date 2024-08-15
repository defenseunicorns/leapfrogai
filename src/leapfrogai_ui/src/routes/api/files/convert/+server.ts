import { error } from '@sveltejs/kit';
import libre from 'libreoffice-convert';
import { promisify } from 'util';
import { stringIdSchema } from '$schemas/chat';
import { getOpenAiClient } from '$lib/server/constants';
import type { RequestHandler } from './$types';
import { stringIdOrFileSchema } from '$schemas/files';
import type { FileObject } from 'openai/resources/files';

// Note - this throws a warning, but it seems erroneous as libre.convert does not return a promise and this is
// IAW with the documentation:
// (node:18447) [DEP0174] DeprecationWarning: Calling promisify on a function that returns a Promise is likely a mistake.
const convertAsync = promisify(libre.convert);

/**
 * Converts a file to PDF.
 * Accepts a file id in the body or a File in the form data
 */

// TODO updates tests to test accept file or id
export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }


  let id: string = '';
  let file: FormDataEntryValue | null = null;
  let contentType = request.headers.get('content-type');

  if (contentType && contentType.includes('application/json')) {
    // Handle JSON request
    try {
      const requestData = await request.json();
      id = requestData.id;
    } catch (e) {
      console.error('Error parsing JSON:', e);
      return error(400, 'Bad Request');
    }
  } else if (contentType && contentType.includes('multipart/form-data')) {
    // Handle FormData request
    try {
      const formData = await request.formData();
      file = formData.get('file');
    } catch (e) {
      console.error('Error parsing FormData:', e);
      return error(400, 'Bad Request');
    }
  } else {
    return error(400, 'Unsupported Content-Type');
  }

  const openai = getOpenAiClient(session.access_token);
  let fileMetadata: FileObject;
  let fileArrayBuffer: ArrayBuffer;
  let filename: string;

  if (id) {
    fileMetadata = await openai.files.retrieve(id);
    if (!fileMetadata) error(404, 'File Not Found');
    filename = fileMetadata.filename;

    let fileRes: Response;
    try {
      fileRes = await openai.files.content(id);
      fileArrayBuffer = await fileRes.arrayBuffer();
    } catch (e) {
      console.error(`Error getting file content for file ${JSON.stringify(fileMetadata)}: `, e);
      error(500, 'Internal Error');
    }
  } else {
    if (!file || !(file instanceof File)) {
      return error(400, { message: 'No file provided or invalid file format' });
    }
    filename = file.name;
    fileArrayBuffer = await file.arrayBuffer();
  }

  if (fileArrayBuffer) {
    try {
      const ext = '.pdf';
      const pdfBuf = await convertAsync(Buffer.from(fileArrayBuffer), ext, undefined);

      return new Response(pdfBuf, {
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': `attachment; filename="${filename}${ext}"`
        }
      });
    } catch (e) {
      console.error('file conversion error', e);
      error(500, 'Internal Error');
    }
  } else error(404, 'File Not Found');
};
