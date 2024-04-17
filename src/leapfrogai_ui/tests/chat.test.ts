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
	test.use({ defaultBrowserType: 'chromium' }); // This sets the browser to Chrome for this test

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

function countWords(str: string) {
	return str.trim().split(/\s+/).length;
}

test('it cancels responses', async ({ page }) => {
	const newMessage = 'write me a long poem';
	await loadPage(page);
	const messages = page.getByTestId('message');
	await sendMessage(page, newMessage);
	await page.waitForTimeout(500);
	await page.getByLabel('cancel', { exact: true }).click();
	await expect(messages).toHaveCount(2);
	const allMessages = await messages.all();
	const response = allMessages[1];
	const responseText = await response.textContent();
	expect(countWords(responseText!)).toBeLessThan(30);
	await deleteConversation(page, newMessage);
});

test('it cancels responses when clicking enter instead of pause button and does not send next message', async ({
	page,
	browserName
}) => {
	// Firefox starts with all this tests conversations loaded even though they should have been deleted by
	// previous browsers when they finished this test. This causes the test to fail because there are multiple
	// conversations with the same label and it doesn't know which one to delete. The other browsers do not do this.
	if (browserName !== 'firefox') {
		const newMessage = 'write me a long poem';
		await loadPage(page);
		const messages = page.getByTestId('message');
		await sendMessage(page, newMessage);
		await page.getByLabel('message input').fill('new question');
		await page.waitForTimeout(500);
		await page.keyboard.down('Enter');
		await page.waitForTimeout(200); // wait to ensure new question was not send
		await expect(messages).toHaveCount(2);
		const allMessages = await messages.all();
		const response = allMessages[1];
		const responseText = await response.textContent();
		expect(countWords(responseText!)).toBeLessThan(30);
		await deleteConversation(page, newMessage);
	}
});
