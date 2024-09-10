import { test as teardown } from './fixtures';
import { cleanup } from './helpers/cleanup';

teardown('teardown', async ({ openAIClient }) => {
  console.log('cleaning up...');
  await cleanup(openAIClient);
  console.log('clean up complete');
});
