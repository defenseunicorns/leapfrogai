import { fail } from '@sveltejs/kit';
import { superValidate, withFiles } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import type { FileObject } from 'openai/resources/files';
import { openai } from '$lib/server/constants';
import { filesSchema } from '$schemas/files';
import type { FileRow } from '$lib/types/files';
import { getUnixSeconds } from '$helpers/dates';

export const actions = {
  default: async ({ request, locals: { safeGetSession } }) => {
    const { session } = await safeGetSession();
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    const form = await superValidate(request, yup(filesSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    if (form.data.files) {
      const uploadedFiles: Array<FileObject | FileRow> = [];
      for (const file of form.data.files) {
        if (file) {
          try {
            const uploadedFile = await openai.files.create({
              file: file,
              purpose: 'assistants'
            });
            uploadedFiles.push(uploadedFile);
          } catch (e) {
            console.error(`Error uploading file ${file.name}: ${e}`);
            const item: FileRow = {
              id: `${file.name}-error-${new Date()}`,
              filename: file.name,
              created_at: getUnixSeconds(new Date()),
              status: 'error'
            };

            uploadedFiles.push(item);
          }
        }
      }

      return withFiles({ form, uploadedFiles });
    }
  }
};
