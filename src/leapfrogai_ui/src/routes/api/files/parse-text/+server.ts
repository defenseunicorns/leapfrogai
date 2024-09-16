import type { RequestHandler } from './$types';
import * as mupdf from 'mupdf';
import { error, json } from '@sveltejs/kit';
import { fileSchema } from '$schemas/files';
import { shortenFileName } from '$helpers/stringHelpers';
import type { LFFile } from '$lib/types/files';

export const POST: RequestHandler = async ({ request, fetch, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let file: LFFile | null;
  // Validate request body
  try {
    const formData = await request.formData();
    file = formData.get('file') as LFFile;
    await fileSchema.validate({ file }, { abortEarly: false });
  } catch (e) {
    console.error('Validation error:', e);
    error(400, `Bad Request, File invalid: ${e}`);
  }

  try {
    let text = '';
    let buffer: ArrayBuffer;
    const contentType = file.type;
    if (contentType !== 'application/pdf') {
      // Convert file to PDF
      const formData = new FormData();
      formData.append('file', file);
      const convertRes = await fetch('/api/files/convert', {
        method: 'POST',
        body: formData
      });

      if (!convertRes.ok) {
        return error(500, { message: 'Error converting file', id: file.id });
      }

      const convertedFileBlob = await convertRes.blob();
      buffer = await convertedFileBlob.arrayBuffer();
    } else buffer = await file.arrayBuffer();

    const document = mupdf.Document.openDocument(buffer, 'application/pdf');
    let i = 0;
    while (i < document.countPages()) {
      const page = document.loadPage(i);
      const json = page.toStructuredText('preserve-whitespace').asJSON();
      for (const block of JSON.parse(json).blocks) {
        for (const line of block.lines) {
          text += line.text;
        }
      }
      i++;
    }

    return json({
      text
    });
  } catch (e) {
    console.error('file parse error', e);
    error(500, { message: 'Internal Error', id: file.id });
  }
};
