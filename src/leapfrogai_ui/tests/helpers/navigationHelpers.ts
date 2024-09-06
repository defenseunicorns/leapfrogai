import { expect } from '../fixtures';
import { delay } from 'msw';
import type { Page } from '@playwright/test';

/** NOTE:
 *  If you test depends on Supabase realtime listeners, you need to wait a second after navigating via
 *  a page.goto call, because the listeners get re-setup when the page is fully reloaded
 * **/

export const loadChatPage = async (page: Page) => {
  await page.goto('/chat');
  await page.waitForURL('/chat');
  await expect(page).toHaveTitle('LeapfrogAI - Chat');
};

export const loadFileManagementPage = async (page: Page) => {
  await page.goto('/chat/file-management');
  await expect(page).toHaveTitle('LeapfrogAI - File Management');
  await delay(1000); // wait for realtime subscriptions to be established
};
export const loadApiKeyPage = async (page: Page) => {
  await page.goto('/chat/api-keys');
  await page.waitForURL('/chat/api-keys');
  await expect(page).toHaveTitle('LeapfrogAI - API Keys');
};

// These navigation helpers do not trigger an app reload

export const navigateToChatPage = async (page: Page) => {
  await page.getByTestId('logo-link').click();
};

export const navigateToFileManagementPage = async (page: Page) => {
  await page.getByTestId('header-settings-btn').click();
  await page.getByText('File Management').click();
};
