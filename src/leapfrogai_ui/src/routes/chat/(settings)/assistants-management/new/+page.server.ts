import { setError, superValidate } from 'sveltekit-superforms';
import { fail, redirect } from '@sveltejs/kit';
import { v4 as uuidv4 } from 'uuid';
import { yup } from 'sveltekit-superforms/adapters';
import { assistantsStore, toastStore } from '$stores';
import type { PageServerLoad } from './$types';
import { supabaseAssistantInputSchema } from '../../../../../schemas/assistants';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '$lib/constants';
import { env } from '$env/dynamic/private';

export const load: PageServerLoad = async ({ locals: { getSession } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const form = await superValidate(
    { temperature: DEFAULT_ASSISTANT_TEMP },
    yup(supabaseAssistantInputSchema)
  );

  return { title: 'LeapfrogAI - New Assistant', form };
};

export const actions = {
  default: async ({ request, locals: { supabase, getSession } }) => {
    // Validate session
    const session = await getSession();
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    let avatarFilePath: string = '';

    const form = await superValidate(request, yup(supabaseAssistantInputSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    if (form.data.avatar) {
      // save avatar
      const filePath = `${session.user.id}/assistant_avatars/${uuidv4()}/${form.data.avatar.name}`;

      const { data: supabaseData, error } = await supabase.storage
        .from('assistant_avatars')
        .upload(filePath, form.data.avatar);

      if (error) {
        console.error('Error saving assistant avatar:', error);
        //Important: Because file objects cannot be serialized, you must return the form using fail, message or setError imported from Superforms
        return setError(form, 'avatar', 'Error saving assistant avatar.');
      }

      avatarFilePath = supabaseData.path;
    }

    // Create assistant object
    const assistant: Partial<Assistant> = {
      name: form.data.name,
      description: form.data.description,
      instructions: form.data.instructions,
      temperature: form.data.temperature,
      model: env.DEFAULT_MODEL,
      metadata: {
        ...assistantDefaults.metadata,
        data_sources: form.data.data_sources || '',
        avatar: avatarFilePath,
        pictogram: form.data.pictogram,
        created_by: session.user.id
      }
    };

    // Save assistant
    const { error: responseError, data: createdAssistant } = await supabase
      .from('assistants')
      .insert(assistant)
      .select()
      .returns<Assistant[]>();

    toastStore.addToast({
      kind: 'success',
      title: 'Assistant Created.',
      subtitle: ''
    });

    if (responseError) {
      console.error('Error saving assistant:', responseError);
      throw new Error('Error saving assistant');
    }

    assistantsStore.addAssistant(createdAssistant[0]);

    return redirect(303, '/chat/assistants-management');
  }
};
