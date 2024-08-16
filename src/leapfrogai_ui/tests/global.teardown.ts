import { test as teardown } from './fixtures';
import { cleanup } from './helpers/cleanup';

// teardown not necessary in CI testing envs
if (process.env.TEST_ENV !== 'CI') {
  teardown('teardown', async ({ openAIClient }) => {
    console.log('cleaning up...');
    await cleanup(openAIClient);
    console.log('clean up complete');
  });
}
