import { expect, type Page } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.PUBLIC_SUPABASE_URL!, process.env.SERVICE_ROLE_KEY!);

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
	await page.click('button[type="submit"]');
};

export const deleteConversationsByLabel = async (labels: string[]) => {
	await supabase.from('conversations').delete().in('label', labels);
};

export const waitForResponseToComplete = async (page: Page) => {
	await expect(page.getByLabel('cancel message')).toHaveCount(1, { timeout: 25000 });
	await expect(page.getByLabel('cancel message')).toHaveCount(0, { timeout: 25000 });
	await expect(page.getByLabel('send')).toHaveCount(1, { timeout: 25000 });
};
