import { test } from '@playwright/test';
import { cleanup } from './helpers/cleanup';
import { getOpenAIClient } from './fixtures';

test('teardown', async () => {
  const openAIClient = await getOpenAIClient();
  console.log('cleaning up...');
  await cleanup(openAIClient);
  console.log('clean up complete');
});
