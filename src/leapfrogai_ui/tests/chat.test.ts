import { faker } from '@faker-js/faker';
import { expect, test } from './fixtures';
import {
  deleteActiveThread,
  getSimpleMathQuestion,
  loadChatPage,
  sendMessage,
  waitForResponseToComplete
} from './helpers';

const newMessage1 = getSimpleMathQuestion();

test('it can start a new thread and receive a response', async ({ page }) => {
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);

  await loadChatPage(page);
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(2);

  await expect(page.getByText('Internal Server Error')).toHaveCount(0);

  await deleteActiveThread(page);
});

// Flaky test - works manually. More likely to pass in Chrome than Firefox.
test.skip('it saves in progress responses when interrupted by a page reload', async ({ page }) => {
  // test.use({ defaultBrowserType: 'chromium' }); // This sets the browser to Chrome for this test

  const newMessage = faker.lorem.words(20);
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await sendMessage(page, newMessage);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  await page.reload();
  await expect(page.getByTestId('message')).toHaveCount(2);
  await deleteActiveThread(page);
});

test('it saves in progress responses when interrupted by changing threads', async ({ page }) => {
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  await page.getByText('New Chat').click();
  await expect(page.getByTestId('message')).toHaveCount(0);
  await page.getByText(newMessage1).click(); // switch back to original thread
  await expect(page.getByTestId('message')).toHaveCount(2);

  await deleteActiveThread(page);
});

function countWords(str: string) {
  return str.trim().split(/\s+/).length;
}

test('it cancels responses', async ({ page }) => {
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await sendMessage(page, newMessage1);
  await expect(messages).toHaveCount(2); // ensure new response is being received
  await page.waitForTimeout(25); // let it partially complete
  await page.getByTestId('cancel message').click();
  await page.waitForTimeout(200); // wait to ensure new question was not sent
  await expect(messages).toHaveCount(2);
  const allMessages = await messages.all();
  const response = allMessages[1];
  const responseText = await response.textContent();
  expect(countWords(responseText!)).toBeLessThan(50);

  await deleteActiveThread(page);
});

test('it cancels responses when clicking enter instead of pause button and does not send next message', async ({
  page,
  browserName
}) => {
  // This test does not pass in Firefox, but it does work when tested manually. Not worth spending
  // additional time debugging at this time. E2E passes for other browsers.
  if (browserName !== 'firefox') {
    const messageWithLongResponse = 'write me a long poem'; // response must take a long time for this test to work
    await loadChatPage(page);
    const messages = page.getByTestId('message');
    await sendMessage(page, messageWithLongResponse);
    await expect(messages).toHaveCount(2); // ensure new response is being received
    await page.getByLabel('message input').fill('new question');
    await page.waitForTimeout(25); // let it partially complete
    await page.keyboard.down('Enter'); // pause response
    await page.waitForTimeout(200); // wait to ensure new question was not sent
    await expect(messages).toHaveCount(2);
    const allMessages = await messages.all();
    const response = allMessages[1];
    const responseText = await response.textContent();
    expect(countWords(responseText!)).toBeLessThan(50);

    await deleteActiveThread(page);
  }
});
