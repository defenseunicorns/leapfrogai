import { faker } from '@faker-js/faker';
import { expect, test } from '@playwright/test';
import {
  clickToDeleteThread,
  deleteActiveThread,
  getSimpleMathQuestion,
  loadChatPage,
  sendMessage,
  waitForResponseToComplete
} from './helpers';

const newMessage1 = getSimpleMathQuestion();
const newMessage2 = getSimpleMathQuestion();
const newMessage3 = getSimpleMathQuestion();

test('it can delete threads', async ({ page }) => {
  await loadChatPage(page);

  const threadLocator = page.getByText(newMessage1);

  await sendMessage(page, newMessage1);
  await clickToDeleteThread(page, newMessage1);
  await expect(threadLocator).toHaveCount(0);
});

test('can edit thread labels', async ({ page }) => {
  const newLabel = faker.lorem.words(3);

  await loadChatPage(page);

  const messages = page.getByTestId('message');
  await sendMessage(page, newMessage1);
  await expect(messages).toHaveCount(2);

  const overflowMenu = page.getByTestId(`overflow-menu-${newMessage1}`);
  await overflowMenu.click();

  await overflowMenu.getByText('Edit').click();

  await page.getByLabel('edit thread').fill(newLabel);

  await page.keyboard.down('Enter');

  await page.reload();

  const threadId = page.url().split('/chat/')[1];

  expect(page.getByTestId(`thread-label-${threadId}`).getByText(newLabel));

  await deleteActiveThread(page);
});

test('Can switch threads', async ({ page }) => {
  await loadChatPage(page);
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(2);

  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(4);

  await page.getByText('New Chat').click();
  await sendMessage(page, newMessage3);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  await page.getByText(newMessage1).click(); // switch threads by clicking thread label

  await expect(messages).toHaveCount(4);

  // cleanup
  await deleteActiveThread(page); // delete thread 1
  await page.getByText(newMessage3).click(); //switch to thread 2
  await expect(messages).toHaveCount(2); // confirm thread 2
  await deleteActiveThread(page); // delete thread 2
});
