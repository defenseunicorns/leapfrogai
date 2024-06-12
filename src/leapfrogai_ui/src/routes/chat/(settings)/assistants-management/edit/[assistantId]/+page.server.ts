import { error, fail, redirect } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { editAssistantInputSchema } from '$lib/schemas/assistants';
import { env } from '$env/dynamic/private';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '$lib/constants';
import { openai } from '$lib/server/constants';
import type { EditAssistantInput, LFAssistant } from '$lib/types/assistants';
import { getAssistantAvatarUrl } from '$helpers/assistants';
import type { AssistantCreateParams } from 'openai/resources/beta/assistants';
import type { APIPromise } from 'openai/core';
import type { VectorStoreFile, VectorStoreFileDeleted } from 'openai/resources/beta/vector-stores';

export const load = async ({ fetch, depends, params, locals: { safeGetSession } }) => {
  depends('lf:files');

  const { session } = await safeGetSession();

  if (!session) {
    throw redirect(303, '/');
  }

  const promises: [Promise<LFAssistant>, Promise<Response>] = [
    openai.beta.assistants.retrieve(params.assistantId) as Promise<LFAssistant>,
    fetch('/api/files')
  ];

  const [assistant, filesRes] = await Promise.all(promises);
  const files = await filesRes.json();

  if (!assistant) {
    error(404, { message: 'Assistant not found.' });
  }
  const vectorStoreId = assistant.tool_resources?.file_search?.vector_store_ids[0];
  let file_ids: string[] = [];
  if (vectorStoreId) {
    try {
      const vectorStoreFiles = await openai.beta.vectorStores.files.list(vectorStoreId);
      file_ids = vectorStoreFiles.data.map((file) => file.id);
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

  return { title: 'LeapfrogAI - Edit Assistant', form, assistant, files };
};

export const actions = {
  default: async ({ request, locals: { supabase, safeGetSession } }) => {
    // Validate session
    const { session } = await safeGetSession();
    if (!session) {
      return fail(401, { message: 'Unauthorized' });
    }

    const form = await superValidate(request, yup(editAssistantInputSchema));

    if (!form.valid) {
      return fail(400, { form });
    }

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
          .from('avatars')
          .remove(['folder/avatar1.png']);

        if (deleteAvatarError) return fail(500, { message: 'error deleting avatar' });
      }
    }

    const data_sources =
      form.data.data_sources &&
      form.data.data_sources.length > 0 &&
      typeof form.data.data_sources[0] === 'string'
        ? form.data.data_sources[0].split(',')
        : [];

    let vectorStoreId: string = form.data.vectorStoreId;
    if (data_sources.length > 0 && (!vectorStoreId || vectorStoreId === 'undefined')) {
      const vectorStore = await openai.beta.vectorStores.create({
        name: `${form.data.name}-vector-store`
      });
      vectorStoreId = vectorStore.id;
    }

    // undefined vector store id from form is passed as a string
    if (vectorStoreId && vectorStoreId !== 'undefined') {
      try {
        const vectorStoreFilesPage = await openai.beta.vectorStores.files.list(vectorStoreId);
        const vectorStoreFiles = vectorStoreFilesPage.data;
        if (vectorStoreFiles) {
          const vectorStoreFileIds = vectorStoreFiles.map((file) => file.id);
          // delete and add files to vector store
          const filesToDelete = vectorStoreFileIds.filter(
            (fileId) => !data_sources.includes(fileId)
          );
          const filesToAdd = data_sources.filter((fileId) => !vectorStoreFileIds.includes(fileId));
          const promises: APIPromise<VectorStoreFileDeleted | VectorStoreFile>[] = [];

          for (const file_id of filesToDelete) {
            promises.push(openai.beta.vectorStores.files.del(vectorStoreId, file_id));
          }
          for (const file_id of filesToAdd) {
            promises.push(
              openai.beta.vectorStores.files.create(vectorStoreId, {
                file_id
              })
            );
          }
          await Promise.all(promises);
        }
      } catch (e) {
        console.error('Error updating vector store', e);
        return fail(500, { message: 'Error updating assistant.' });
      }
    }

    // Create assistant object
    const assistant: AssistantCreateParams = {
      name: form.data.name,
      description: form.data.description,
      instructions: form.data.instructions,
      temperature: form.data.temperature,
      model: env.DEFAULT_MODEL,
      tools: data_sources && data_sources.length > 0 ? [{ type: 'file_search' }] : [],
      tool_resources:
        data_sources && data_sources.length > 0
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

    return redirect(303, '/chat/assistants-management');
  }
};
