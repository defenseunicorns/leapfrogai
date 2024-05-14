import { superValidate } from 'sveltekit-superforms';
import { fail, redirect } from '@sveltejs/kit';
import { yup } from 'sveltekit-superforms/adapters';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '$lib/constants';
import { env } from '$env/dynamic/private';
import type { PageServerLoad } from './$types';
import { supabaseAssistantInputSchema } from '../../../../../schemas/assistants';

export const load: PageServerLoad = async ({ locals: { getSession } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const form = await superValidate(
    { temperature: DEFAULT_ASSISTANT_TEMP },
    yup(supabaseAssistantInputSchema),
    { errors: false } // turn off errors for new assistant b/c providing default data turns them on
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

    let savedAvatarFilePath: string = '';

    const form = await superValidate(request, yup(supabaseAssistantInputSchema));

    if (!form.valid) {
      return fail(400, { form });
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
        pictogram: form.data.pictogram,
        created_by: session.user.id
        // avatar is added in later with an update call
      }
    };

    // Create assistant
    const { error: responseError, data: createdAssistant } = await supabase
      .from('assistants')
      .insert(assistant)
      .select()
      .returns<Assistant[]>()
      .single();

    if (responseError) {
      console.error('Error saving assistant:', responseError);
      return fail(500, { message: 'Error saving assistant.' });
    }

    if (form.data.avatar) {
      // save avatar
      const filePath = createdAssistant.id;

      const { data: supabaseData, error } = await supabase.storage
        .from('assistant_avatars')
        .upload(filePath, form.data.avatar);

      if (error) {
        console.error('Error saving assistant avatar:', error);
        return fail(500, { message: 'Error saving assistant avatar.' });
      }

      savedAvatarFilePath = supabaseData.path;
    }

    if (form.data.avatar) {
      const { error: updateAssistantError } = await supabase
        .from('assistants')
        .update({ metadata: { ...createdAssistant.metadata, avatar: savedAvatarFilePath } })
        .eq('id', createdAssistant.id);

      if (updateAssistantError) return fail(500, { message: 'Error adding avatar to assistant.' });
    }


    return redirect(303, '/chat/assistants-management');
  }
};
