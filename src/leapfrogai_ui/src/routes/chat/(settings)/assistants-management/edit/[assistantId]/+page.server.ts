import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import type { PageServerLoad } from './$types';
import { yup } from 'sveltekit-superforms/adapters';
import { editAssistantInputSchema } from '$lib/schemas/assistants';
import { env } from '$env/dynamic/private';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '$lib/constants';

export const load: PageServerLoad = async ({ params, locals: { getSession, supabase } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }
  const { data: assistant, error: assistantError } = await supabase
    .from('assistants')
    .select()
    .eq('id', params.assistantId)
    .returns<Assistant[]>()
    .single();

  if (assistantError) {
    error(404, { message: 'Assistant not found.' });
  }

  const assistantFormData: EditAssistantInput = {
    id: assistant.id,
    name: assistant.name || '',
    description: assistant.description || '',
    instructions: assistant.instructions || '',
    temperature: assistant.temperature || DEFAULT_ASSISTANT_TEMP,
    data_sources: assistant.metadata.data_sources,
    pictogram: assistant.metadata.pictogram
    // note - the avatar is a string location of the file, not a file type, it is handled by the component instead
  };

  const form = await superValidate(assistantFormData, yup(editAssistantInputSchema));

  return { title: 'LeapfrogAI - Edit Assistant', form, assistant };
};

export const actions = {
  default: async ({ request, locals: { supabase, getSession } }) => {
    // Validate session
    const session = await getSession();
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    let savedAvatarFilePath: string = '';

    const form = await superValidate(request, yup(editAssistantInputSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    const { error: getAssistantError } = await supabase
      .from('assistants')
      .select()
      .eq('id', form.data.id)
      .returns<Assistant[]>()
      .single();

    if (getAssistantError) return fail(404, { message: 'Assistant not found.' });

    // Update avatar
    if (form.data.avatar) {
      const filePath = form.data.id;

      const { data: supabaseData, error } = await supabase.storage
        .from('assistant_avatars')
        .upload(filePath, form.data.avatar, { upsert: true });

      if (error) {
        console.error('Error updating assistant avatar:', error);
        return fail(500, { message: 'Error updating assistant avatar.' });
      }

      savedAvatarFilePath = supabaseData.path;
    } else {
      // Delete avatar
      const { error: deleteAvatarError } = await supabase.storage
        .from('avatars')
        .remove(['folder/avatar1.png']);
      if (deleteAvatarError) return fail(500, { message: 'error deleting avatar' });
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
        avatar: savedAvatarFilePath,
        pictogram: form.data.pictogram,
        created_by: session.user.id
      }
    };

    // Save assistant
    const { error: responseError } = await supabase
      .from('assistants')
      .update(assistant)
      .eq('id', form.data.id)
      .returns<Assistant[]>()
      .single();

    if (responseError) {
      console.error('Error updating assistant:', responseError);
      return fail(500, { message: 'Error updating assistant.' });
    }

    return redirect(303, '/chat/assistants-management');
  }
};
