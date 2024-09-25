import { test } from '@playwright/test';
import { cleanup } from './helpers/cleanup';
import { getOpenAIClient } from './fixtures';
import fs from 'node:fs';

test('teardown', async () => {
  const openAIClient = await getOpenAIClient();
  console.log('cleaning up...');
  await cleanup(openAIClient);
  // Check if the auth file exists and delete it
  const filePath = 'playwright/.auth/user.json';
  if (fs.existsSync(filePath)) {
    fs.unlink(filePath, (err) => {
      if (err) {
        console.error('Error deleting the auth file:', err);
      } else {
        console.log('Auth file deleted successfully.');
      }
    });
  } else {
    console.log('Auth file not found.');
  }
  console.log('clean up complete');
});
