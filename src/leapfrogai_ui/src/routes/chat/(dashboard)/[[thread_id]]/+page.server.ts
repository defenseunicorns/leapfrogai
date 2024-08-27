import * as mupdf from 'mupdf';
import { fail, superValidate, withFiles } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import type { Actions } from './$types';
import { filesSchema } from '$schemas/files';
import type { FileMetadata } from '$lib/types/files';
import { env } from '$env/dynamic/public';
import { shortenFileName } from '$helpers/stringHelpers';

// Ensure there is buffer to include the user's message in the context window. If the user types more than the number
// of characters allowed below, the frontend will handle it and truncate the extractedFilesText
// and pop a warning toast notification.
const ADJUSTED_MAX = Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT) - 5000;

export const actions: Actions = {
  // Handles parsing text from files, will convert file to pdf if is not already
  default: async ({ request, fetch, locals: { session } }) => {
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    const form = await superValidate(request, yup(filesSchema));

    if (!form.valid) {
      console.log(
        'Files form action: Invalid form submission.',
        'id:',
        form.id,
        'errors:',
        form.errors
      );
      return fail(400, { form });
    }

    const extractedFilesText: FileMetadata[] = [];

    if (form.data.files && form.data.files.length > 0) {
      try {
        for (const file of form.data.files) {
          let text = '';
          if (file) {
            try {
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
                  const resJson = await convertRes.json();
                  return fail(500, { form, message: resJson.message });
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

              extractedFilesText.push({
                name: shortenFileName(file.name),
                type: file.type,
                text,
                status: 'complete'
              });

              // If this file adds too much text (larger than allowed max), remove the text and set to error status
              let totalTextLength = extractedFilesText.reduce(
                (acc, fileMetadata) => acc + JSON.stringify(fileMetadata).length,
                0
              );
              if (totalTextLength > ADJUSTED_MAX) {
                extractedFilesText[extractedFilesText.length - 1] = {
                  name: shortenFileName(file.name),
                  type: file.type,
                  text: '',
                  status: 'error',
                  errorText: 'Error: Upload fewer or smaller files'
                };
              }
            } catch (e) {
              console.error(`Error uploading file: ${file}: ${e}`);
              extractedFilesText.push({
                name: shortenFileName(file.name),
                type: file.type,
                text: '',
                status: 'error',
                errorText: 'Error uploading file'
              });
            }
          }
        }
        return withFiles({ extractedFilesText, form });
      } catch (e) {
        console.error(e);
        return fail(500, { form });
      }
    }
    return fail(400, { form });
  }
};
