import { deleteAllGeneratedFixtureFiles, deleteAllTestFilesWithApi } from './fileHelpers';
import { deleteAllAssistants, deleteAssistantAvatars } from './assistantHelpers';
import { deleteAllTestThreadsWithApi } from './threadHelpers';
import type OpenAI from 'openai';
import { deleteAllTestAPIKeys } from './apiHelpers';

export const cleanup = async (openAIClient: OpenAI) => {
  deleteAllGeneratedFixtureFiles();
  await deleteAllTestFilesWithApi(openAIClient);
  await deleteAllAssistants(openAIClient);
  await deleteAllTestThreadsWithApi(openAIClient);
  await deleteAssistantAvatars();
  await deleteAllTestAPIKeys();
};
