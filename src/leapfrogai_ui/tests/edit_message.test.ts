import { faker } from '@faker-js/faker';
import { expect, test } from './fixtures';
import { loadChatPage, sendMessage, waitForResponseToComplete } from './helpers';
import { delay } from 'msw';

test('editing a message', async ({ page }) => {
	const newMessage1 = faker.lorem.words(3);
	const newMessage2 = faker.lorem.words(3);
	await loadChatPage(page);

	await sendMessage(page, newMessage1);
	await waitForResponseToComplete(page);
	await sendMessage(page, newMessage2);
	await waitForResponseToComplete(page);

	// Edit first message
	await page.getByTestId('message').first().click();
	await page.getByLabel('edit prompt').first().click();
	await page.getByLabel('edit message input').fill('edited message');
	await page.getByLabel('submit edited message').click();
	await delay(3000);
	const messages = page.getByTestId('message');

	// Expect same number of total messages (including new response)
	await expect(messages).toHaveCount(4);

	// Ensure original first message was deleted and is now the second message
	const firstMessage = page.getByTestId('message').nth(0);
	const firstMessageTextContent = await firstMessage.textContent();
	expect(firstMessageTextContent?.trim()).toEqual(newMessage2);

	// Check the third message is now the edited message
	const editedMessage = page.getByTestId('message').nth(2);
	const textContent = await editedMessage.textContent();
	expect(textContent?.trim()).toEqual('edited message');
});

test('editing a message when an AI response is missing', async ({ page }) => {
	let isFirstRequest = true;
	const newMessage1 = faker.lorem.words(3);
	const newMessage2 = faker.lorem.words(3);

	await page.route('*/**/api/chat', async (route) => {
		if (isFirstRequest) {
			isFirstRequest = false;
            await route.abort('failed');
		} else {
			await route.continue();
		}
	});

	await loadChatPage(page);
	try {
		await sendMessage(page, newMessage1);
	} catch {
		console.log('simulated network failure');
	}
	// Reload page to see original message (vercel AI SDK removes it from the messages store on failure, but it does
	// get saved to the DB
	await delay(1000);
	await page.reload();

	const messages = page.getByTestId('message');
    await expect(messages).toHaveCount(1);

    // Send a second message that gets a successful response
	await sendMessage(page, newMessage2);
	await waitForResponseToComplete(page);

	await expect(messages).toHaveCount(3); // no AI response for first message

	await page.getByTestId('message').first().click();
	await page.getByLabel('edit prompt').first().click();
	await page.getByLabel('edit message input').fill('edited message');
	await page.getByLabel('submit edited message').click();
	await delay(3000);

    // Expect 4 messages now with successful response
    await expect(messages).toHaveCount(4);

    // Ensure original first message was deleted and is now the second message
    const firstMessage = page.getByTestId('message').nth(0);
    const firstMessageTextContent = await firstMessage.textContent();
    expect(firstMessageTextContent?.trim()).toEqual(newMessage2);

    // Check the third message is now the edited message
    const editedMessage = page.getByTestId('message').nth(2);
    const textContent = await editedMessage.textContent();
    expect(textContent?.trim()).toEqual('edited message');
});

test("regenerating responses", async ({page}) => {
	const newMessage1 = faker.lorem.words(3);

	await loadChatPage(page);


	await sendMessage(page, newMessage1);
	await waitForResponseToComplete(page);

	const messages = page.getByTestId('message');
	await expect(messages).toHaveCount(2);

	await page.getByLabel('regenerate message').click();
	await expect(messages).toHaveCount(1);
	await waitForResponseToComplete(page);
	await expect(messages).toHaveCount(2);
})