import { superValidate, withFiles } from 'sveltekit-superforms';
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';
import { yup } from 'sveltekit-superforms/adapters';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '$lib/constants';
import { env } from '$env/dynamic/private';
import { assistantInputSchema } from '$lib/schemas/assistants';
import type { LFAssistant } from '$lib/types/assistants';
import { getAssistantAvatarUrl } from '$helpers/assistants';
import type { AssistantCreateParams } from 'openai/resources/beta/assistants';
import { getOpenAiClient } from '$lib/server/constants';
import { filesSchema } from '$schemas/files';
import type { VectorStore } from 'openai/resources/beta/vector-stores/index';

export const load: PageServerLoad = async () => {
  // Populate form with default temperature
  const form = await superValidate(
    { temperature: DEFAULT_ASSISTANT_TEMP },
    yup(assistantInputSchema),
    { errors: false } // turn off errors for new assistant b/c providing default data turns them on
  );

  const filesForm = await superValidate({}, yup(filesSchema), { errors: false });

  return { title: 'LeapfrogAI - New Assistant', form, filesForm };
};

export const actions: Actions = {
  default: async ({ request, locals: { supabase, session } }) => {
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    const form = await superValidate(request, yup(assistantInputSchema));
    if (!form.valid) {
      return fail(400, { form });
    }

    const data_sources =
      form.data.data_sources &&
      form.data.data_sources.length > 0 &&
      typeof form.data.data_sources[0] === 'string'
        ? form.data.data_sources[0].split(',')
        : [];

    const openai = getOpenAiClient(session.access_token);

    let vectorStore: VectorStore | undefined = undefined;
    if (data_sources && data_sources.length > 0) {
      try {
        vectorStore = await openai.beta.vectorStores.create({
          name: `${form.data.name}-vector-store`,
          file_ids: data_sources
        });
      } catch (e) {
        console.error('Error creating vector store', e);
        return fail(500, { message: 'Error creating vector store.' });
      }
    }

    // Create assistant object, we can't spread the form data here because we need to re-nest some of the values
    const assistant: AssistantCreateParams = {
      name: form.data.name,
      description: form.data.description,
      instructions: form.data.instructions,
      temperature: form.data.temperature,
      model: env.DEFAULT_MODEL,
      tools: data_sources && data_sources.length > 0 ? [{ type: 'file_search' }] : undefined,
      tool_resources: vectorStore
        ? {
            file_search: {
              vector_store_ids: [vectorStore.id]
            }
          }
        : null,
      metadata: {
        ...assistantDefaults.metadata,
        pictogram: form.data.pictogram,
        user_id: session.user.id
        // avatar is added in later with an update call after saving to supabase
      }
    };

    // Create assistant
    let createdAssistant: LFAssistant;
    try {
      createdAssistant = (await openai.beta.assistants.create(assistant)) as LFAssistant;
    } catch (e) {
      console.error(`Error creating assistant: ${e}`);
      return fail(500, { message: 'Error creating assistant.' });
    }

    // save avatar
    if (form.data.avatarFile) {
      const filePath = createdAssistant.id;

      const { error } = await supabase.storage
        .from('assistant_avatars')
        .upload(filePath, form.data.avatarFile);

      if (error) {
        console.error('Error saving assistant avatar:', error);
        return fail(500, { message: 'Error saving assistant avatar.' });
      }
      // update assistant with saved avatar path
      try {
        createdAssistant = (await openai.beta.assistants.update(createdAssistant.id, {
          metadata: {
            ...(createdAssistant.metadata ? createdAssistant.metadata : undefined),
            avatar: getAssistantAvatarUrl(filePath)
          }
        })) as LFAssistant;
      } catch (e) {
        console.error(`Error adding avatar to assistant: ${e}`);
        return fail(500, { message: 'Error adding avatar to assistant.' });
      }
    }
    return withFiles({
      form,
      assistant: createdAssistant,
      fileIds: data_sources,
      redirectUrl: '/chat/assistants-management'
    });
  }
};
