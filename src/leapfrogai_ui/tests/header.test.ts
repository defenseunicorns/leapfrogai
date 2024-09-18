import { expect, test } from './fixtures';
import {
  deleteActiveThread,
  getLastUrlParam,
  sendMessage,
  waitForResponseToComplete
} from './helpers/threadHelpers';
import { getSimpleMathQuestion } from './helpers/helpers';

test('it only shows the open/close sidebar button on small screens', async ({ page }) => {
  await page.setViewportSize({ width: 600, height: 600 });
  await page.goto('/chat');
  await expect(page.getByTestId('open-sidebar-btn')).toBeVisible();

  await page.setViewportSize({ width: 1800, height: 800 });
  await expect(page.getByTestId('open-sidebar-btn')).not.toBeVisible();
  await expect(page.getByTestId('close-sidebar-btn')).not.toBeVisible();
});

test('it opens the sidebar when the open/close sidebar button is clicked', async ({ page }) => {
  await page.setViewportSize({ width: 600, height: 600 });
  await page.goto('/chat');

  await page.getByTestId('open-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).toBeVisible();
  await page.getByTestId('close-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).not.toBeVisible();
  await page.getByTestId('open-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).toBeVisible();
});

test('does not show the menu open/close btn non-chat pages', async ({ page }) => {
  await page.setViewportSize({ width: 600, height: 600 });
  await page.goto('/chat');

  await page.getByTestId('open-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).toBeVisible();

  await page.goto('/chat/api-keys');

  await expect(page.getByTestId('open-sidebar-btn')).not.toBeVisible();
  await expect(page.getByTestId('close-sidebar-btn')).not.toBeVisible();
});

test('shows the menu open/close btn on chat thread pages', async ({ page, openAIClient }) => {
  // Test it also shows on an active thread (not just /chat)
  await page.goto('/chat');
  await sendMessage(page, getSimpleMathQuestion());
  await waitForResponseToComplete(page);
  const threadId = getLastUrlParam(page);
  expect(threadId).toBeDefined();
  await page.setViewportSize({ width: 600, height: 600 });
  await page.goto(`/chat/${threadId}`); // reload page, dynamic resizing won't be detected in playwright
  await page.getByTestId('open-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).toBeVisible();
  await deleteActiveThread(page, openAIClient);
});
