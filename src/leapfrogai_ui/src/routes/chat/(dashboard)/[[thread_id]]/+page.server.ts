import * as mupdf from 'mupdf';
import type { Actions } from './$types';
import { fail, superValidate, withFiles } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { filesSchema } from '$schemas/files';

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
      for (const file of form.data.files) {
        if (file) {
          const buffer = await file.arrayBuffer();
          const document = mupdf.Document.openDocument(buffer, 'application/pdf');
          let i = 0;
          while (i < document.countPages()) {
            const page = document.loadPage(i);
            const json = page.toStructuredText('preserve-whitespace').asJSON();
            for (const block of JSON.parse(json).blocks) {
              for (const line of block.lines) {
                console.log('adding', line.text);
                text += line.text;
              }
            }
            i++;
          }
        }
      }

      return withFiles({ text, form });
    }
    return fail(400, { form });
  }
};
