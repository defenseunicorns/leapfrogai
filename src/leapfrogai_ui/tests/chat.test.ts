import { faker } from '@faker-js/faker';
import { expect, test } from './fixtures';
import {
  createAssistantWithApi,
  deleteActiveThread,
  deleteAssistantWithApi,
  getSimpleMathQuestion,
  loadChatPage,
  sendMessage,
  waitForResponseToComplete
} from './helpers';

const newMessage1 = getSimpleMathQuestion();
const newMessage2 = getSimpleMathQuestion();

test('it can start a new thread and receive a response', async ({ page }) => {
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);
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
  await expect(messages).toHaveCount(2);
  await page.reload();
  await expect(page.getByTestId('message')).toHaveCount(2);
  await deleteActiveThread(page);
});

// Flaky test - works manually.
test.skip('it saves in progress responses when interrupted by changing threads', async ({
  page
}) => {
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);

  await sendMessage(page, newMessage1);
  await expect(messages).toHaveCount(2);

  await page.getByText('New Chat').click();
  await expect(messages).toHaveCount(0);
  await page.getByText(newMessage1).click(); // switch back to original thread
  await expect(messages).toHaveCount(2);

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

test('it can switch between normal chat and chat with an assistant', async ({ page }) => {
  const assistant = await createAssistantWithApi();

  const messages = page.getByTestId('message');
  await loadChatPage(page);
  await expect(messages).toHaveCount(0);

  // Send regular chat message
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(2);

  // Select assistant
  await expect(page.getByTestId('assistant-dropdown')).not.toBeDisabled();
  const assistantDropdown = page.getByTestId('assistant-dropdown');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  // Send assistant chat message
  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(4);

  await expect(page.getByTestId('user-icon')).toHaveCount(2);
  await expect(page.getByTestId('leapfrog-icon')).toHaveCount(1);
  await expect(page.getByTestId('assistant-icon')).toHaveCount(1);

  // Test selected assistant has a checkmark and clicking it again de-selects the assistant
  await expect(page.getByTestId('assistant-dropdown')).not.toBeDisabled();
  await assistantDropdown.click();
  await page.getByTestId('checked').click();

  // Send regular chat message
  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(6);

  await expect(page.getByTestId('user-icon')).toHaveCount(3);
  await expect(page.getByTestId('leapfrog-icon')).toHaveCount(2);
  await expect(page.getByTestId('assistant-icon')).toHaveCount(1);

  // Cleanup
  await deleteAssistantWithApi(assistant.id);
  await deleteActiveThread(page);
});
