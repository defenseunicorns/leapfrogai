import * as mupdf from 'mupdf';
import type { Actions } from './$types';
import { fail, superValidate, withFiles } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';
import { delay } from 'msw';
import { Form } from 'docx/build/file/drawing/inline/graphic/graphic-data/pic/shape-properties/form';
// TODO - convert file to pdf if not pdf
export const actions: Actions = {
  default: async ({ request, locals: { session } }) => {
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

    if (form.data.files && form.data.files.length > 0) {
      let text = '';
      try {
        for (const file of form.data.files) {
          if (file) {
            let buffer: ArrayBuffer;
            const contentType = file.type;
            if (contentType !== 'application/pdf') { // Convert file to PDF
              const formData = new FormData();
              formData.append('file', file);
              const convertRes = await fetch('/api/files/convert', {
                method: 'POST',
                body: formData
              });
              if (!convertRes.ok) fail(500, { form });

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
          }
        }
        return withFiles({ text, form });
      } catch {
        return fail(500, form);
      }
    }
    return fail(400, { form });
  }
};
