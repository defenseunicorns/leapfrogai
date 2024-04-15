import { expect, test } from '@playwright/test';
import { loadChatPage } from './helpers';
import { getFakeConversation } from '../src/testUtils/fakeData';

test('it can import and exports conversations', async ({ page }) => {
	const conversation = getFakeConversation();
	const conversationStr = JSON.stringify([conversation]);

	await loadChatPage(page);

	await page.getByLabel('Import data').setInputFiles({
		name: 'upload.json',
		mimeType: 'application/JSON',
		buffer: Buffer.from(conversationStr)
	});
	await expect(page.getByText(conversation.label)).toHaveCount(1);

	const downloadPromise = page.waitForEvent('download');
	await page.getByText('Export data').click();

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
	const importedConversation = parsedDownload.find((c: Conversation) => c.id === conversation.id);
	expect(importedConversation).toEqual(conversation);
});
