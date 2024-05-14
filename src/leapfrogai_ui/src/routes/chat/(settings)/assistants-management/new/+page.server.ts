import type { PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { supabaseAssistantInputSchema } from '../../../../../schemas/assistants';
import { assistantDefaults, AVATAR_FILE_SIZE_ERROR_TEXT, MAX_AVATAR_SIZE } from '$lib/constants';
import { env } from '$env/dynamic/private';
import { v4 as uuidv4 } from 'uuid';
import { assistantsStore } from '$stores';
import { ValidationError } from 'yup';

export const load: PageServerLoad = async ({ locals: { getSession } }) => {
  const session = await getSession();

  if (!session) {
    throw redirect(303, '/');
  }

  return { title: 'LeapfrogAI - New Assistant' };
};

export const actions = {
  default: async ({ request, locals: { supabase, getSession } }) => {
    // Validate session
    const session = await getSession();
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    // Build Assistant Input object
    const formData = await request.formData();

    const name = formData.get('name') as string;
    const description = formData.get('description') as string;
    const instructions = formData.get('instructions') as string;
    const temperature = formData.get('temperature') as string;
    const data_sources = formData.get('data_sources') as string | undefined;
    const avatarFile = formData.get('avatar') as File | undefined;
    const pictogram = formData.get('pictogram') as string | undefined;

    const assistantInput: NewAssistantInput = {
      name,
      description,
      instructions,
      temperature: Number(temperature),
      data_sources,
      pictogram
    };
    let avatarFilePath: string = '';

    // Validate Assistant Input Object
    try {
      await supabaseAssistantInputSchema.validate(assistantInput, { abortEarly: false });
    } catch (e) {
      if (e instanceof ValidationError) {
        const errors: { [key: string]: string } = {};
        e.inner.forEach((innerVal) => {
          if (innerVal.path) {
            errors[innerVal.path] = innerVal.errors[0];
          }
        });

        console.error(
          `Form submission: create assistant validation errors: ${JSON.stringify(errors)}`
        );
        return fail(400, { message: 'Bad Request', errors });
      }
      return fail(500, { message: 'Internal Server Error' });
    }

    // Upload Avatar
    if (avatarFile?.size !== 0) {
      if (!(avatarFile instanceof File)) {
        return fail(400, { message: 'Invalid avatar' });
      }
      // Validate file type
      const validExtensions = ['.jpeg', '.jpg', '.png'];
      const fileExtension = avatarFile.name.match(/\.[0-9a-z]+$/i);
      if (!fileExtension || !validExtensions.includes(fileExtension[0].toLowerCase())) {
        return fail(400, {
          message: 'Invalid file type, accepted types are: ' + validExtensions.join(', ')
        });
      }

      if (avatarFile.size > MAX_AVATAR_SIZE)
        return fail(400, { message: AVATAR_FILE_SIZE_ERROR_TEXT });

      const filePath = `${session.user.id}/assistant_avatars/${uuidv4()}/${avatarFile.name}`;

      const { data: supabaseData, error } = await supabase.storage
        .from('assistant_avatars')
        .upload(filePath, avatarFile);

      if (error) {
        console.error('Error uploading to Supabase:', error);
        return fail(500, { message: 'Error uploading file' });
      }

      avatarFilePath = supabaseData.path;
    }

    // Create Assistant Object
    const assistant: Omit<Assistant, 'id' | 'created_at'> = {
      ...assistantDefaults,
      name: assistantInput.name,
      description: assistantInput.description,
      instructions: assistantInput.instructions,
      temperature: assistantInput.temperature,
      model: env.DEFAULT_MODEL,
      metadata: {
        ...assistantDefaults.metadata,
        data_sources: assistantInput.data_sources || '',
        avatar: avatarFilePath,
        pictogram: assistantInput.pictogram,
        created_by: session.user.id
      }
    };

    // Save Assistant
    const { error: responseError, data: createdAssistant } = await supabase
      .from('assistants')
      .insert(assistant)
      .select()
      .returns<Assistant[]>();

    if (responseError) {
      console.log(
        `error creating assistant,  error status: ${responseError.code}: ${responseError.message}`
      );
      return fail(500, { message: 'Internal Server Error' });
    }

    assistantsStore.addAssistant(createdAssistant[0]);

    return redirect(303, '/chat/assistants-management');
  }
};
