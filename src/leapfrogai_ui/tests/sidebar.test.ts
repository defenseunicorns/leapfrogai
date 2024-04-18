import { faker } from '@faker-js/faker';
import { expect, test} from './fixtures';
import { loadChatPage, sendMessage } from './helpers';
import { deleteConversation } from './helpers';

test.beforeEach(async ({ clearDb }) => {
	await clearDb();
});

test('it can delete conversations', async ({ page }) => {
	const newMessage = faker.lorem.words(3);
	await loadChatPage(page);

	const conversationLocator = page.getByText(newMessage);

	await sendMessage(page, newMessage);
	await deleteConversation(page, newMessage);
	await expect(conversationLocator).toHaveCount(0);
});

test('can edit conversation labels', async ({ page }) => {
	const newMessage = faker.lorem.words(3);
	const newLabel = faker.lorem.words(3);

	await loadChatPage(page);

	const messages = page.getByTestId('message');
	await sendMessage(page, newMessage);
	await expect(messages).toHaveCount(2);

	const overflowMenu = page.getByTestId(`overflow-menu-${newMessage}`);
	await overflowMenu.click();

	await overflowMenu.getByText('Edit').click();

	await page.getByLabel('edit conversation').fill(newLabel);

	await page.keyboard.down('Enter');

	await page.reload();

	const conversationId = page.url().split('/chat/')[1];

	expect(page.getByTestId(`conversation-label-${conversationId}`).getByText(newLabel));
});

// TODO - this is now broken (related to type="submit" on cancel button?
test('Can switch conversation threads', async ({ page }) => {
	const newMessage1 = faker.lorem.words(3);
	const newMessage2 = faker.lorem.words(3);
	const newMessage3 = faker.lorem.words(3);
	await loadChatPage(page);
	await sendMessage(page, newMessage1);

	const messages = page.getByTestId('message');
	await expect(messages).toHaveCount(2); // wait for AI response
	await expect(page.getByLabel('cancel')).toHaveCount(0); // wait for response to finish
	await sendMessage(page, newMessage2);
	await expect(messages).toHaveCount(4);
	await expect(page.getByLabel('cancel')).toHaveCount(0); // wait for response to finish

	await page.getByText('New Chat').click();
	await sendMessage(page, newMessage3);
	await expect(messages).toHaveCount(2);
	await expect(page.getByLabel('cancel')).toHaveCount(0); // wait for response to finish

	await page.getByText(newMessage1).click(); // switch conversations by clicking conversation label

	await expect(messages).toHaveCount(4);
});
