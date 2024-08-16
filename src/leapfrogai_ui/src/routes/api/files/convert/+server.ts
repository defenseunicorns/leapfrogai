import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { convertFileToPdf } from './[id]/utils';

/**
 * Converts a file to PDF.
 * Accepts a File in the form data
 */
export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let file: FormDataEntryValue | null = null;

  // Handle FormData request
  try {
    const formData = await request.formData();
    file = formData.get('file');
  } catch (e) {
    console.error('Error parsing FormData:', e);
    return error(400, 'Bad Request');
  }

  if (!file || !(file instanceof File)) {
    return error(400, { message: 'No file provided or invalid file format' });
  }

  let fileArrayBuffer: ArrayBuffer;
  let filename: string;

  filename = file.name;
  fileArrayBuffer = await file.arrayBuffer();
  if (!fileArrayBuffer) error(404, 'File Not Found');
  try {
    return await convertFileToPdf(fileArrayBuffer, filename);
  } catch (e) {
    console.error('file conversion error', e);
    error(500, 'Internal Error');
  }
};
