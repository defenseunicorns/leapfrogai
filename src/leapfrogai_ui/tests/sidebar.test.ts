import { expect, test } from './fixtures';
import { getSimpleMathQuestion } from './helpers/helpers';
import {
  clickToDeleteThread,
  deleteActiveThread,
  sendMessage,
  waitForResponseToComplete
} from './helpers/threadHelpers';
import { loadChatPage } from './helpers/navigationHelpers';

const newMessage1 = getSimpleMathQuestion();
const newMessage2 = getSimpleMathQuestion();
const newMessage3 = getSimpleMathQuestion();

test('it can delete threads', async ({ page }) => {
  await loadChatPage(page);

  const threadLocator = page.getByRole('button', { name: newMessage1 });

  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);

  await clickToDeleteThread(page, newMessage1);
  await expect(threadLocator).toHaveCount(0);
});

test('can edit thread labels', async ({ page, openAIClient }) => {
  const newLabel = getSimpleMathQuestion();

  await loadChatPage(page);

  const messages = page.getByTestId('message');
  await sendMessage(page, newMessage1);
  await expect(messages).toHaveCount(2);

  const threads = page.getByTestId('threads');
  await threads.getByText(newMessage1).hover();
  const threadMenuBtn = page.getByTestId(`thread-menu-btn-${newMessage1}`);
  await threadMenuBtn.click();

  await page.getByTestId('sidebar-popover').getByRole('button', { name: /edit/i }).click();

  await page.getByTestId('edit-thread-input').fill(newLabel);

  await page.keyboard.down('Enter');

  await page.reload();

  expect(page.getByTestId(`thread-menu-btn-${newLabel}`).getByText(newLabel));

  await deleteActiveThread(page, openAIClient);
});

test('Can switch threads', async ({ page, openAIClient }) => {
  await loadChatPage(page);
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(2);

  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(4);

  await page.getByText('New chat').click();
  await expect(messages).toHaveCount(0);
  await sendMessage(page, newMessage3);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  await page.getByRole('button', { name: newMessage1 }).click(); // switch threads by clicking thread label

  await expect(messages).toHaveCount(4);

  // cleanup
  await deleteActiveThread(page, openAIClient); // delete thread 1
  await page.getByText(newMessage3).click(); //switch to thread 2
  await expect(messages).toHaveCount(2); // confirm thread 2
  await deleteActiveThread(page, openAIClient); // delete thread 2
});
