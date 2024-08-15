
import type { Actions } from './$types';
import { fail, superValidate } from 'sveltekit-superforms';
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
      let texts: string[] = [];
      for (const file of form.data.files) {
        if (file) {
          const buffer = await file.arrayBuffer();
          // const data = await pdf(Buffer.from(buffer));
          // texts.push(data.text);
        }
      }

      return { texts, form };
    }
    return fail(400, { form });
  }
};
