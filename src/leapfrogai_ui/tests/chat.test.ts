import { faker } from '@faker-js/faker';
import { expect, type Page, test } from '@playwright/test';
import { deleteConversation, sendMessage } from './helpers';

const loadPage = async (page: Page) => {
	await page.goto('/chat');
	await expect(page).toHaveTitle('LeapfrogAI - Chat');
};

test('it can start a new conversation and receive a response', async ({ page }) => {
	const newMessage = faker.lorem.words(3);
	let messages = await page.getByTestId('message');
	await expect(messages).toHaveCount(0);

	await loadPage(page);
	await sendMessage(page, newMessage);

	messages = await page.getByTestId('message');
	await expect(messages).toHaveCount(2);

	await expect(page.getByText('Internal Server Error')).toHaveCount(0);

	await deleteConversation(page, newMessage);
});

// Flaky test - works manually. More likely to pass in Chrome than Firefox.
test.skip('it saves in progress responses when interrupted by a page reload', async ({ page }) => {
	test.use({ defaultBrowserType: 'chromium' }); // This sets the browser to Firefox for this test

	const newMessage = faker.lorem.words(20);
	await loadPage(page);
	const messages = page.getByTestId('message');
	await sendMessage(page, newMessage);
	await expect(messages).toHaveCount(2);

	await page.reload();
	await expect(page.getByTestId('message')).toHaveCount(2);

	await deleteConversation(page, newMessage);
});

test('it save in progress responses when interrupted by changing threads', async ({ page }) => {
	const newMessage = faker.lorem.words(3);
	await loadPage(page);
	const messages = page.getByTestId('message');
	await sendMessage(page, newMessage);
	await expect(messages).toHaveCount(2);

	await page.getByText('New Chat').click();
	await page.getByText(newMessage).click(); // switch conversations by clicking conversation label
	await expect(page.getByTestId('message')).toHaveCount(2);

	await deleteConversation(page, newMessage);
});
