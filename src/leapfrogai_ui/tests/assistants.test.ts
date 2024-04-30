import { expect, test } from './fixtures';
import { loadChatPage } from './helpers';

test('it navigates to the assistants page', async ({ page }) => {
	await loadChatPage(page);

	await page.getByLabel('Settings').click();
	await page.getByText('Assistants Management').click();

	await expect(page).toHaveTitle('LeapfrogAI - Assistants');
});

test('it has a button that navigates to the new assistant page', async ({ page }) => {
	await page.goto('/chat/assistants-management');

	await page.getByRole('button', { name: 'New Assistant' }).click();
	await page.waitForURL('**/assistants-management/new');
	await expect(page).toHaveTitle('LeapfrogAI - New Assistant');
});
