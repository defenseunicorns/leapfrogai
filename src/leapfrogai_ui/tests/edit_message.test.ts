import { expect, test } from './fixtures';
import { getSimpleMathQuestion, normalizeWhitespace } from './helpers/helpers';
import { delay } from 'msw';
import { createAssistantWithApi, deleteAssistantWithApi } from './helpers/assistantHelpers';
import {
  deleteActiveThread,
  sendMessage,
  waitForResponseToComplete
} from './helpers/threadHelpers';
import { loadChatPage } from './helpers/navigationHelpers';

const newMessage1 = getSimpleMathQuestion();
const newMessage2 = getSimpleMathQuestion();

test('editing a message', async ({ page, openAIClient }) => {
  await loadChatPage(page);

  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);
  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);

  // Edit first message
  await page.getByTestId('message').first().click();
  await expect(page.getByLabel('edit prompt').first()).not.toBeDisabled(); // wait for message to finish saving
  await page.getByLabel('edit prompt').first().click();
  await page.getByTestId('edit-message-input').fill('edited message');
  await page.getByLabel('submit edited message').click();
  await delay(3000);
  const messages = page.getByTestId('message');

  // Expect same number of total messages (including new response)
  await expect(messages).toHaveCount(4);

  // Ensure original first message was deleted and is now the second message
  const firstMessage = page.getByTestId('message').first();
  const firstMessageTextContent = await firstMessage.textContent();
  expect(normalizeWhitespace(firstMessageTextContent!)).toEqual(`You ${newMessage2}`); // 'You' is card header for the user message

  // Check the third message is now the edited message
  const editedMessage = page.getByTestId('message').nth(2);
  const textContent = await editedMessage.textContent();
  expect(normalizeWhitespace(textContent!)).toEqual('You edited message');
  await deleteActiveThread(page, openAIClient);
});

test('editing a message when an AI response is missing', async ({ page, openAIClient }) => {
  let isFirstRequest = true;

  await page.route('*/**/api/chat', async (route) => {
    if (isFirstRequest) {
      isFirstRequest = false;
      await route.abort('failed');
    } else {
      await route.continue();
    }
  });

  await loadChatPage(page);
  try {
    await sendMessage(page, newMessage1);
  } catch {
    console.log('simulated network failure');
  }
  // Reload page to see original message (vercel AI SDK removes it from the messages store on failure, but it does
  // get saved to the DB
  await delay(1000);
  await page.reload();

  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(1);

  // Send a second message that gets a successful response
  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(3); // no AI response for first message

  await page.getByTestId('message').first().click();
  await page.getByLabel('edit prompt').first().click();
  await page.getByTestId('edit-message-input').fill('edited message');
  await page.getByLabel('submit edited message').click();
  await delay(3000);

  // Expect 4 messages now with successful response
  await expect(messages).toHaveCount(4);

  // Ensure original first message was deleted and is now the second message
  const firstMessage = page.getByTestId('message').first();
  const firstMessageTextContent = await firstMessage.textContent();
  expect(normalizeWhitespace(firstMessageTextContent!)).toEqual(`You ${newMessage2}`); // 'You' is card header for the user message

  // Check the third message is now the edited message
  const editedMessage = page.getByTestId('message').nth(2);
  const textContent = await editedMessage.textContent();
  expect(normalizeWhitespace(textContent!)).toEqual('You edited message');
  await deleteActiveThread(page, openAIClient);
});

test('regenerating responses', async ({ page, openAIClient }) => {
  await loadChatPage(page);

  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);

  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(2);

  await expect(page.getByLabel('regenerate message')).not.toBeDisabled(); // wait for message to finish saving
  await page.getByLabel('regenerate message').click();
  await expect(messages).toHaveCount(0);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);
  await deleteActiveThread(page, openAIClient);
});

test('it can regenerate the last assistant response', async ({ page, openAIClient }) => {
  const assistant = await createAssistantWithApi({ openAIClient });

  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);

  await expect(page.getByLabel('regenerate message')).not.toBeDisabled(); // wait for message to finish saving
  await page.getByLabel('regenerate message').click();
  await expect(messages).toHaveCount(0);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  // Cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
  await deleteActiveThread(page, openAIClient);
});

test('editing an assistant message', async ({ page, openAIClient }) => {
  const assistant = await createAssistantWithApi({ openAIClient });

  await loadChatPage(page);

  // Select assistant
  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);
  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);

  // Edit first message

  await page.getByTestId('message').first().click();
  await expect(page.getByLabel('edit prompt').first()).not.toBeDisabled(); // wait for message to finish saving
  await page.getByLabel('edit prompt').first().click();
  await page.getByTestId('edit-message-input').fill('edited message');
  await page.getByLabel('submit edited message').click();
  await delay(3000);
  const messages = page.getByTestId('message');

  // Expect same number of total messages (including new response)
  await expect(messages).toHaveCount(4);

  // Ensure original first message was deleted and is now the second message
  const firstMessage = page.getByTestId('message').first();
  const firstMessageTextContent = await firstMessage.textContent();
  expect(normalizeWhitespace(firstMessageTextContent!)).toEqual(`You ${newMessage2}`); // 'You' is card header for the user message

  // Check the third message is now the edited message
  const editedMessage = page.getByTestId('message').nth(2);
  const textContent = await editedMessage.textContent();
  expect(normalizeWhitespace(textContent!)).toEqual('You edited message');

  await expect(page.getByTestId('user-icon')).toHaveCount(2);
  await expect(page.getByTestId('assistant-icon')).toHaveCount(2);

  // Cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
  await deleteActiveThread(page, openAIClient);
});
