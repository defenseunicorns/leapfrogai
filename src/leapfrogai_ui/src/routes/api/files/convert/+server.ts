import { error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { convertFileToPdf } from './[id]/utils';
import { fileSchema } from '$schemas/files';

/**
 * Converts a file to PDF.
 * Accepts a File in the form data
 */
export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let file: File | null;
  // Validate request body
  try {
    const formData = await request.formData();
    file = formData.get('file') as File;
    await fileSchema.validate({ file }, { abortEarly: false });
  } catch (e) {
    console.error('Validation error:', e);
    error(400, `Bad Request, File invalid: ${e}`);
  }

  try {
    let fileArrayBuffer: ArrayBuffer;
    let filename: string;
    filename = file.name;
    fileArrayBuffer = await file.arrayBuffer();
    if (!fileArrayBuffer) error(404, 'File Not Found');
    return await convertFileToPdf(fileArrayBuffer, filename);
  } catch (e) {
    console.error('file conversion error', e);
    error(500, 'Internal Error');
  }
};
