import yup, { ValidationError } from 'yup';
import type { PageServerLoad } from './$types';
import { type Actions, fail } from '@sveltejs/kit';

export const load: PageServerLoad = async () => {
  return { title: 'LeapfrogAI - New Assistant' };
};

const NewAssistantSchema = yup.object({
  name: yup.string().required('Required'),
  tagline: yup.string(),
  instructions: yup.string().required('Required'),
  temperature: yup.number().required('Required'),
  dataSources: yup.array().of(yup.string())
});

export const actions: Actions = {
  newAssistant: async ({ request }) => {
    const data = Object.fromEntries(await request.formData());

    try {
      await NewAssistantSchema.validate(data, { abortEarly: false });
      // TODO save data to db
      return { success: true };
    } catch (err) {
      if (err instanceof ValidationError) {
        // Convert to [{[keyName]: "error msg"}]
        const errors = err.inner.reduce((acc, err) => {
          return { ...acc, [err.path as string]: err.message };
        }, {});
        return fail(400, { errors });
      }
      console.log(`Internal Error: ${String(err)}`);
      return fail(500);
    }
  }
};
