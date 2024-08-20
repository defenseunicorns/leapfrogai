import { deleteAllGeneratedFixtureFiles, deleteAllTestFilesWithApi } from './fileHelpers';
import { deleteAllAssistants, deleteAssistantAvatars } from './assistantHelpers';
import { deleteAllTestThreadsWithApi } from './threadHelpers';
import type OpenAI from 'openai';

export const cleanup = async (openAIClient: OpenAI) => {
  deleteAllGeneratedFixtureFiles();
  await deleteAllTestFilesWithApi(openAIClient);
  await deleteAllAssistants(openAIClient);
  await deleteAllTestThreadsWithApi(openAIClient);
  await deleteAssistantAvatars();
  // TODO - the deleteAllTestAPIKeys helper uses a leapfrog endpoint that is not authorizing the SERVICE_ROLE_KEY
  // https://github.com/defenseunicorns/leapfrogai/issues/936
  // await deleteAllTestAPIKeys();
};
