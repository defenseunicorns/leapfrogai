import { fail, superValidate, withFiles } from 'sveltekit-superforms';
import type { Actions } from './$types';
import { yup } from 'sveltekit-superforms/adapters';
import type { FileObject } from 'openai/resources/files';
import { filesSchema } from '$schemas/files';
import type { LFFileObject, PendingOrErrorFile } from '$lib/types/files';
import { getUnixSeconds } from '$helpers/dates';
import { getOpenAiClient } from '$lib/server/constants';

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

    const openai = getOpenAiClient(session.access_token);

    if (form.data.files) {
      const fileId: string | null = null;

      let uploadedFiles: Array<FileObject | LFFileObject | PendingOrErrorFile> = [];

      const uploadPromises = form.data.files.map(async (file) => {
        if (file) {
          try {
            // Upload file
            const uploadedFile = await openai.files.create({
              file: file,
              purpose: 'assistants'
            });

            return uploadedFile;
          } catch (e) {
            console.error(`Error uploading file ${file.name}: ${e}`);
            const item: PendingOrErrorFile = {
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
            return item;
          }
        }
        return null;
      });
      uploadedFiles = (await Promise.all(uploadPromises)).filter(
        (file): file is FileObject | LFFileObject => file !== null
      );

      return withFiles({ form, uploadedFiles });
    }
  }
};
