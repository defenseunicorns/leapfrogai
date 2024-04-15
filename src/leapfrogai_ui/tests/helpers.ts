import { expect, type Page } from '@playwright/test';

export const loadChatPage = async (page: Page) => {
	await page.goto('/chat');
	await expect(page).toHaveTitle('LeapfrogAI - Chat');
};


export const deleteConversation = async (page: Page, label: string) => {
	await page.getByTestId(`overflow-menu-${label}`).click();
	await page.getByTestId(`overflow-menu-delete-${label}`).click();

	await page.locator('button:text("Delete")').click();
	await expect(page.getByTestId(`overflow-menu-${label}`)).toHaveCount(0);
};

export const sendMessage = async (page: Page, message = 'Who are Defense Unicorns?') => {
	await page.getByLabel('message input').fill(message);
	// timeout is to wait for possible previous response to finish so send button is re-enabled
	await page.click('button[type="submit"]', { timeout: 20000 });
};
