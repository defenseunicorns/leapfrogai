import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import type { Assistant } from 'openai/resources/beta/assistants';
import { filesCheckSchema } from '$schemas/files';
import { getOpenAiClient } from '$lib/server/constants';

export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  // Validate request body
  let requestData: { fileIds: string[] };
  try {
    requestData = await request.json();
    const isValid = await filesCheckSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  try {
    const openai = getOpenAiClient(session.access_token);

    const affectedAssistants: Assistant[] = [];

    const myAssistantsPage = await openai.beta.assistants.list();
    const myAssistants = myAssistantsPage.data;

    for (const assistant of myAssistants) {
      let assistantAffected = false;
      const vectorStoreIds = assistant.tool_resources?.file_search?.vector_store_ids;

      if (vectorStoreIds && vectorStoreIds.length > 0) {
        for (const vectorStoreId of vectorStoreIds) {
          if (assistantAffected) break; // only add assistant once if affected
          const vectorStoreFiles = await openai.beta.vectorStores.files.list(vectorStoreId);
          const vectorStoreFileIds = vectorStoreFiles.data.map((file) => file.id);

          for (const fileId of requestData.fileIds) {
            if (vectorStoreFileIds.includes(fileId)) {
              affectedAssistants.push(assistant);
              assistantAffected = true;
              break;
            }
          }
        }
      }
    }

    return json(affectedAssistants);
  } catch (e) {
    console.error(`Error checking assistant for deletion: ${e}`);
    error(500, 'Error checking assistant for deletion');
  }
};
