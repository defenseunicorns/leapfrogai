import { deleteAllGeneratedFixtureFiles, deleteAllTestFilesWithApi } from './fileHelpers';
import { deleteAllAssistants, deleteAssistantAvatars } from './assistantHelpers';
import { deleteAllTestThreadsWithApi } from './threadHelpers';
import { deleteAllTestAPIKeys } from './apiHelpers';
import type OpenAI from 'openai';

export const cleanup = async (openAIClient: OpenAI) => {
  deleteAllGeneratedFixtureFiles();
  await deleteAllTestFilesWithApi(openAIClient);
  await deleteAllAssistants(openAIClient);
  await deleteAllTestThreadsWithApi(openAIClient);
  await deleteAssistantAvatars();
  await deleteAllTestAPIKeys();
};
