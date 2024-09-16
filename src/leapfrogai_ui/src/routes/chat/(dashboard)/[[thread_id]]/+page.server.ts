import * as mupdf from 'mupdf';
import { fail, superValidate, withFiles } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import type { Actions } from './$types';
import { filesSchema } from '$schemas/files';
import type { FileMetadata } from '$lib/types/files';
import { env } from '$env/dynamic/public';
import { shortenFileName } from '$helpers/stringHelpers';
import { APPROX_MAX_CHARACTERS, FILE_UPLOAD_PROMPT } from '$constants';
import { ERROR_UPLOADING_FILE_MSG, FILE_CONTEXT_TOO_LARGE_ERROR_MSG } from '$constants/errors';
import { v4 as uuidv4 } from 'uuid';

// Ensure length of file context message does not exceed total context window when including the
// file upload prompt, user's message, and string quotes
const ADJUSTED_MAX =
  APPROX_MAX_CHARACTERS - Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT) - FILE_UPLOAD_PROMPT.length - 2;

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
      for (const file of form.data.files) {
        console.log("Server side file", file)
        let text = '';
        if (file) {
          try {
            let buffer: ArrayBuffer;
            const contentType = file.type;

            // Skip audio files
            if (contentType.startsWith('audio/')) {
              extractedFilesText.push({
                id: file.id,
                name: shortenFileName(file.name),
                type: file.type,
                text: 'Audio file contents were not processed',
                status: 'complete'
              });
              continue;
            }
            if (contentType !== 'application/pdf') {
              // Convert file to PDF
              const formData = new FormData();
              formData.append('file', file);
              const convertRes = await fetch('/api/files/convert', {
                method: 'POST',
                body: formData
              });

              if (!convertRes.ok) {
                throw new Error('Error converting file'); //caught locally
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
              id: file.id,
              name: shortenFileName(file.name),
              type: file.type,
              text,
              status: 'complete'
            });

            // If this file adds too much text (larger than allowed max), remove the text and set to error status
            const totalTextLength = extractedFilesText.reduce(
              (acc, fileMetadata) => acc + JSON.stringify(fileMetadata).length,
              0
            );
            if (totalTextLength > ADJUSTED_MAX) {
              extractedFilesText[extractedFilesText.length - 1] = {
                id: file.id,
                name: shortenFileName(file.name),
                type: file.type,
                text: '',
                status: 'error',
                errorText: FILE_CONTEXT_TOO_LARGE_ERROR_MSG
              };
            }
          } catch (e) {
            console.error(`Error uploading file: ${file}: ${e}`);
            extractedFilesText.push({
              id: file.id,
              name: shortenFileName(file.name),
              type: file.type,
              text: '',
              status: 'error',
              errorText: ERROR_UPLOADING_FILE_MSG
            });
          }
        }
      }

      return withFiles({ extractedFilesText, form });
    }
    return fail(400, { form });
  }
};
