import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate, withFiles } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { editAssistantInputSchema } from '$lib/schemas/assistants';
import { env } from '$env/dynamic/private';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '$lib/constants';
import type { EditAssistantInput, LFAssistant } from '$lib/types/assistants';
import { getAssistantAvatarUrl } from '$helpers/assistants';
import type { AssistantCreateParams } from 'openai/resources/beta/assistants';
import { filesSchema } from '$schemas/files';
import type { APIPromise } from 'openai/core';
import type {
  VectorStoreFile,
  VectorStoreFileDeleted
} from 'openai/resources/beta/vector-stores/files';
import { getOpenAiClient } from '$lib/server/constants';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, locals: { session } }) => {
  if (!session) {
    throw redirect(303, '/');
  }

  const openai = getOpenAiClient(session.access_token);

  const assistant = (await openai.beta.assistants.retrieve(params.assistantId)) as LFAssistant;

  if (!assistant) {
    error(404, { message: 'Assistant not found.' });
  }

  const vectorStoreId =
    assistant.tool_resources?.file_search?.vector_store_ids &&
    assistant.tool_resources?.file_search?.vector_store_ids[0];
  let file_ids: string[] = [];
  if (vectorStoreId) {
    try {
      const vectorStoreFiles = await openai.beta.vectorStores.files.list(vectorStoreId);
      file_ids = vectorStoreFiles.data
        .filter((file) => file.status === 'completed')
        .map((file) => file.id);
    } catch (e) {
      console.error(`Error getting vector store files: ${e}`);
    }
  }

  const assistantFormData: EditAssistantInput = {
    id: assistant.id,
    name: assistant.name || '',
    description: assistant.description || '',
    instructions: assistant.instructions || '',
    temperature: assistant.temperature || DEFAULT_ASSISTANT_TEMP,
    data_sources: file_ids,
    pictogram: assistant.metadata.pictogram,
    avatar: assistant.metadata.avatar,
    avatarFile: null
  };

  const form = await superValidate(assistantFormData, yup(editAssistantInputSchema));
  const filesForm = await superValidate({}, yup(filesSchema), { errors: false });

  return { title: 'LeapfrogAI - Edit Assistant', form, filesForm, assistant };
};

export const actions: Actions = {
  default: async ({ request, locals: { supabase, session } }) => {
    // Validate session
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    const form = await superValidate(request, yup(editAssistantInputSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

    const openai = getOpenAiClient(session.access_token);
    const deleteAvatar = !form.data.avatar && !form.data.avatarFile;
    const filePath = form.data.id;

    // Update avatar if new file uploaded
    if (form.data.avatarFile) {
      const { error } = await supabase.storage
        .from('assistant_avatars')
        .upload(filePath, form.data.avatarFile, { upsert: true });

      if (error) {
        console.error('Error updating assistant avatar:', error);
        return fail(500, { message: 'Error updating assistant avatar.' });
      }
    } else {
      if (!form.data.avatar) {
        // Delete avatar
        const { error: deleteAvatarError } = await supabase.storage
          .from('assistant_avatars')
          .remove([`${filePath}`]);
        if (deleteAvatarError) {
          console.error('Error deleting assistant avatar:', deleteAvatarError);
          return fail(500, { message: 'error deleting avatar' });
        }
      }
    }

    const data_sources =
      form.data.data_sources &&
      form.data.data_sources.length > 0 &&
      typeof form.data.data_sources[0] === 'string'
        ? form.data.data_sources[0].split(',')
        : [];

    let vectorStoreId = form.data.vectorStoreId;
    if (vectorStoreId === 'undefined') vectorStoreId = undefined;

    if (vectorStoreId) {
      try {
        const vectorStoreFilesPage = await openai.beta.vectorStores.files.list(vectorStoreId);
        const vectorStoreFiles = vectorStoreFilesPage.data;

        const vectorStoreFileIds = vectorStoreFiles.map((file) => file.id);
        // delete and add files to vector store
        const filesToDelete = vectorStoreFileIds.filter((fileId) => !data_sources.includes(fileId));
        const filesToAdd = data_sources.filter((fileId) => !vectorStoreFileIds.includes(fileId));
        const promises: APIPromise<VectorStoreFileDeleted | VectorStoreFile>[] = [];

        for (const file_id of filesToDelete) {
          await openai.beta.vectorStores.files.del(vectorStoreId, file_id);
        }
        for (const file_id of filesToAdd) {
          await openai.beta.vectorStores.files.create(vectorStoreId, {
            file_id
          });
        }

        await Promise.all(promises);
      } catch (e) {
        console.error('Error updating vector store', e);
        return fail(500, { message: 'Error updating assistant.' });
      }
    } else {
      // Create new vector store with files
      if (data_sources.length > 0) {
        try {
          const vectorStore = await openai.beta.vectorStores.create({
            name: `${form.data.name}-vector-store`,
            file_ids: data_sources
          });
          vectorStoreId = vectorStore.id;
        } catch (e) {
          console.error('Error creating vector store', e);
          return fail(500, { message: 'Error creating vector store.' });
        }
      }
    }

    // Create assistant object
    const assistant: AssistantCreateParams = {
      name: form.data.name,
      description: form.data.description,
      instructions: form.data.instructions,
      temperature: form.data.temperature,
      model: env.DEFAULT_MODEL,
      tools: data_sources && data_sources.length > 0 ? [{ type: 'file_search' }] : undefined,
      tool_resources: vectorStoreId
        ? {
            file_search: {
              vector_store_ids: [vectorStoreId]
            }
          }
        : null,
      metadata: {
        ...assistantDefaults.metadata,
        avatar: deleteAvatar ? '' : getAssistantAvatarUrl(filePath),
        pictogram: form.data.pictogram,
        user_id: session.user.id
      }
    };

    // Update assistant
    try {
      await openai.beta.assistants.update(form.data.id, assistant);
    } catch (e) {
      console.error(`Error updating assistant: ${e}`);
      return fail(500, { message: 'Error updating assistant.' });
    }
    return withFiles({
      form,
      assistant,
      fileIds: data_sources,
      redirectUrl: '/chat/assistants-management'
    });
  }
};
