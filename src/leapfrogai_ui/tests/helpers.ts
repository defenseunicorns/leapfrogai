import { expect, type Page } from '@playwright/test';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.PUBLIC_SUPABASE_URL!, process.env.SERVICE_ROLE_KEY!);

export const loadChatPage = async (page: Page) => {
  await page.goto('/chat');
  await page.waitForURL('/chat');
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

// Note - this will not apply the temperature slider value provided, it only clicks on the 0.5 increment
export const createAssistant = async (page: Page, assistantInput: NewAssistantInput) => {
  await page.goto('/chat/assistants-management/new');
  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);
  await page.locator('.bx--slider__track').click();

  await page.getByRole('button', { name: 'Save' }).click();
};

export const deleteConversationsByLabel = async (labels: string[]) => {
  await supabase.from('conversations').delete().in('label', labels);
};

export const waitForResponseToComplete = async (page: Page) => {
  await expect(page.getByTestId('cancel message')).toHaveCount(1, { timeout: 25000 });
  await expect(page.getByTestId('cancel message')).toHaveCount(0, { timeout: 25000 });
  await expect(page.getByTestId('send message')).toHaveCount(1, { timeout: 25000 });
};

export const deleteAssistantByName = async (name: string) => {
  await supabase.from('conversations').delete().eq('name', name);
};
