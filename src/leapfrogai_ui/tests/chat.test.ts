import { faker } from '@faker-js/faker';
import { test, expect, type Page } from './fixtures';
import { sendMessage } from './helpers';

const loadPage = async (page: Page) => {
	await page.goto('/chat');
	await expect(page).toHaveTitle('LeapfrogAI - Chat');
};

test.beforeEach(async ({ clearDb }) => {
	await clearDb();
});

test('it can start a new conversation and receive a response', async ({ page }) => {
	const newMessage = faker.lorem.words(3);
	let messages = await page.getByTestId('message');
	await expect(messages).toHaveCount(0);

	await loadPage(page);
	await sendMessage(page, newMessage);

	messages = await page.getByTestId('message');
	await expect(messages).toHaveCount(2);

	await expect(page.getByText('Internal Server Error')).toHaveCount(0);
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
});

test('it saves in progress responses when interrupted by changing threads', async ({ page }) => {
	const newMessage = faker.lorem.words(3);
	await loadPage(page);
	const messages = page.getByTestId('message');
	await sendMessage(page, newMessage);
	await expect(messages).toHaveCount(2);

	await page.getByText('New Chat').click();
	await expect(page.getByTestId('message')).toHaveCount(0);
	await page.getByText(newMessage).click(); // switch back to original thread
	await expect(page.getByTestId('message')).toHaveCount(2);
});

function countWords(str: string) {
	return str.trim().split(/\s+/).length;
}

test('it cancels responses', async ({ page }) => {
	const newMessage = 'write me a long poem';
	await loadPage(page);
	const messages = page.getByTestId('message');
	await sendMessage(page, newMessage);
	await expect(messages).toHaveCount(2); // ensure new response is being received
	await page.waitForTimeout(300); // let it partially complete
	await page.getByLabel('cancel', { exact: true }).click();
	await page.waitForTimeout(200); // wait to ensure new question was not sent
	await expect(messages).toHaveCount(2);
	const allMessages = await messages.all();
	const response = allMessages[1];
	const responseText = await response.textContent();
	expect(countWords(responseText!)).toBeLessThan(30);
});

test('it cancels responses when clicking enter instead of pause button and does not send next message', async ({
	page
}) => {
	const newMessage = 'write me a long poem';
	await loadPage(page);
	const messages = page.getByTestId('message');
	await sendMessage(page, newMessage);
	await page.getByLabel('message input').fill('new question');
	await expect(messages).toHaveCount(2); // ensure new response is being received
	await page.waitForTimeout(300); // let it partially complete
	await page.keyboard.down('Enter'); // pause response
	await page.waitForTimeout(200); // wait to ensure new question was not sent
	await expect(messages).toHaveCount(2);
	const allMessages = await messages.all();
	const response = allMessages[1];
	const responseText = await response.textContent();
	expect(countWords(responseText!)).toBeLessThan(50);
});
