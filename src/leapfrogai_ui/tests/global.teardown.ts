import { test as teardown } from './fixtures';
import { deleteAllGeneratedFixtureFiles, deleteAllTestFilesWithApi } from './helpers/fileHelpers';
import { deleteAllAssistants, deleteAssistantAvatars } from './helpers/assistantHelpers';
import { deleteAllTestThreadsWithApi } from './helpers/threadHelpers';
import { deleteAllTestAPIKeys } from './helpers/apiHelpers';

// teardown not necessary in CI testing envs
if (process.env.TEST_ENV !== 'CI') {
  teardown('teardown', async ({ openAIClient }) => {
    console.log('cleaning up...');
    deleteAllGeneratedFixtureFiles();
    await deleteAllTestFilesWithApi(openAIClient);
    await deleteAllAssistants(openAIClient);
    await deleteAllTestThreadsWithApi(openAIClient);
    await deleteAssistantAvatars();
    await deleteAllTestAPIKeys();
    console.log('clean up complete');
  });
}
