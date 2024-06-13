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
      const fileId: string | null = null;

      const uploadedFiles: Array<FileObject | FileRow> = [];
      for (const file of form.data.files) {
        if (file) {
          try {
            // Upload file
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

            try {
              // Cleanup in the event of an error
              if (fileId) {
                // Delete file
                await openai.files.del(fileId);
              }
            } catch (e) {
              console.error(`Error cleaning up file/vector store: ${e}`);
              // fail silently so user still receives item with error status
            }
          }
        }
      }

      return withFiles({ form, uploadedFiles });
    }
  }
};
