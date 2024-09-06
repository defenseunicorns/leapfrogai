import { expect, test } from './fixtures';
import { getFakeThread } from '../testUtils/fakeData';
import type { LFThread } from '$lib/types/threads';
import { loadChatPage } from './helpers/navigationHelpers';

test('it can import and exports threads', async ({ page }) => {
  const thread = getFakeThread();
  const threadStr = JSON.stringify([thread]);

  await loadChatPage(page);

  await page.getByTestId('import-chat-history-input').setInputFiles({
    name: 'upload.json',
    mimeType: 'application/JSON',
    buffer: Buffer.from(threadStr)
  });
  await expect(page.getByText('Importing...')).toBeVisible();
  await expect(page.getByText(thread.metadata.label)).toHaveCount(1);
  await expect(page.getByText('Importing...')).not.toBeVisible();

  const downloadPromise = page.waitForEvent('download');
  await page.getByText('Export chat history').click();

  const download = await downloadPromise;

  let dataStr = '';
  await download.saveAs('/tmp/' + download.suggestedFilename());
  const file = await download.createReadStream();
  file.on('data', (chunk) => {
    dataStr += chunk;
  });
  await new Promise((resolve, reject) => {
    file.on('end', resolve);
    file.on('error', reject);
  });

  const parsedDownload = JSON.parse(dataStr);
  expect(parsedDownload.length).toBeGreaterThan(0);
  const importedThreads = parsedDownload.find(
    (t: LFThread) => t.metadata.label === thread.metadata.label
  );
  // We can't test full equality because the ids and insertedAt dates will be different
  expect(importedThreads).toBeDefined();
});

test('it displays an error toast and removes the Importing spinner on error when the threads are improperly formatted', async ({
  page
}) => {
  const threadStr = JSON.stringify([{ bad: 'data' }]);

  await loadChatPage(page);

  await page.getByTestId('import-chat-history-input').setInputFiles({
    name: 'upload.json',
    mimeType: 'application/JSON',
    buffer: Buffer.from(threadStr)
  });

  await expect(page.getByText('Importing...')).not.toBeVisible();
  await expect(page.getByText('Threads are incorrectly formatted.')).toBeVisible();
});
