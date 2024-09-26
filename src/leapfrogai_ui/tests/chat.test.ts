import { expect, test } from './fixtures';
import { getSimpleMathQuestion, LONG_RESPONSE_PROMPT } from './helpers/helpers';
import { createAssistantWithApi, deleteAssistantWithApi } from './helpers/assistantHelpers';
import {
  deleteActiveThread,
  sendMessage,
  waitForResponseToComplete
} from './helpers/threadHelpers';
import { loadChatPage } from './helpers/navigationHelpers';
import { ERROR_GETTING_ASSISTANT_MSG_TOAST } from '$constants/toastMessages';

const newMessage1 = getSimpleMathQuestion();
const newMessage2 = getSimpleMathQuestion();

test('it can start a new thread and receive a response', async ({ page, openAIClient }) => {
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(2);

  await expect(page.getByText('Internal Server Error')).toHaveCount(0);

  await deleteActiveThread(page, openAIClient);
});

test('it saves in progress responses when interrupted by a page reload', async ({
  page,
  openAIClient
}) => {
  if (process.env.DEFAULT_MODEL === 'llama-cpp-python') {
    test.skip();
  }
  const uniqueLongMessagePrompt = `${LONG_RESPONSE_PROMPT} ${new Date().toISOString()}`;
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await sendMessage(page, uniqueLongMessagePrompt);
  await expect(messages).toHaveCount(2);
  await page.reload();
  await expect(page.getByTestId('message')).toHaveCount(2);
  await deleteActiveThread(page, openAIClient);
});

test('it saves in progress responses when interrupted by changing threads', async ({
  page,
  openAIClient
}) => {
  if (process.env.DEFAULT_MODEL === 'llama-cpp-python') {
    test.skip();
  }
  const uniqueLongMessagePrompt = `${LONG_RESPONSE_PROMPT} ${new Date().toISOString()}`;
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);

  await sendMessage(page, uniqueLongMessagePrompt);
  await expect(messages).toHaveCount(2);

  await page.getByText('New Chat').click();
  await expect(messages).toHaveCount(0);
  await page.getByText(uniqueLongMessagePrompt).click(); // switch back to original thread
  await expect(messages).toHaveCount(2);

  await deleteActiveThread(page, openAIClient);
});

function countWords(str: string) {
  return str.trim().split(/\s+/).length;
}

test('it cancels responses', async ({ page, openAIClient }) => {
  if (process.env.DEFAULT_MODEL === 'llama-cpp-python') {
    test.skip();
  }
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await sendMessage(page, LONG_RESPONSE_PROMPT);
  await expect(messages).toHaveCount(2); // ensure new response is being received
  await page.getByTestId('cancel message').click();
  await page.waitForTimeout(200); // wait to ensure new question was not sent
  await expect(messages).toHaveCount(2);
  const allMessages = await messages.all();
  const response = allMessages[1];
  const responseText = await response.textContent();
  expect(countWords(responseText!)).toBeLessThan(50);

  await deleteActiveThread(page, openAIClient);
});

test('it cancels responses when clicking enter instead of pause button and does not send next message', async ({
  page,
  openAIClient
}) => {
  if (process.env.DEFAULT_MODEL === 'llama-cpp-python') {
    test.skip();
  }
  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await sendMessage(page, LONG_RESPONSE_PROMPT); // response must take a long time for this test to work
  await expect(messages).toHaveCount(2); // ensure new response is being received
  await page.getByTestId('chat-input').fill('new question');
  await page.waitForTimeout(25); // let it partially complete
  await page.keyboard.down('Enter'); // pause response
  await page.waitForTimeout(200); // wait to ensure new question was not sent
  await expect(messages).toHaveCount(2);
  const allMessages = await messages.all();
  const response = allMessages[1];
  const responseText = await response.textContent();
  expect(countWords(responseText!)).toBeLessThan(50);

  await deleteActiveThread(page, openAIClient);
});

// TODO - LeapfrogAI API is currently too slow when sending assistant responses so when this test
// runs with multiple browsers in parallel, it times out. It should usually work for individual
// browsers unless the API is receiving additional run requests simultaneously
test('it can switch between normal chat and chat with an assistant', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });

  await loadChatPage(page);
  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);

  // Send regular chat message
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  // Select assistant
  await expect(page.getByTestId('assistants-select-btn')).not.toBeDisabled();
  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  // Send assistant chat message
  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(4);

  await expect(page.getByTestId('user-icon')).toHaveCount(2);
  await expect(page.getByTestId('leapfrogai-icon')).toHaveCount(1);
  await expect(page.getByTestId('assistant-icon')).toHaveCount(1);

  // Test selected assistant has a checkmark and clicking it again de-selects the assistant
  await expect(page.getByTestId('assistants-select-btn')).not.toBeDisabled();
  await assistantDropdown.click();
  await page.getByTestId('checked').click();

  // Send regular chat message
  await sendMessage(page, newMessage2);
  await waitForResponseToComplete(page);

  await expect(messages).toHaveCount(6);

  await expect(page.getByTestId('user-icon')).toHaveCount(3);
  await expect(page.getByTestId('leapfrogai-icon')).toHaveCount(2);
  await expect(page.getByTestId('assistant-icon')).toHaveCount(1);

  // Cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
  await deleteActiveThread(page, openAIClient);
});

test('it formats code in a code block and can copy the code', async ({ page }) => {
  // note - intent is not to test styling, but to ensure code block is created
  await loadChatPage(page);
  await expect(page.getByTestId('copy-code-btn')).not.toBeVisible();
  await sendMessage(page, 'create a javascript function that prints hello world');
  await waitForResponseToComplete(page);
  const copyBtns = await page.getByTestId('copy-code-btn').all();
  expect(copyBtns.length).toBeGreaterThan(0);
});

test('it can chat with an assistant that doesnt have files', async ({ page, openAIClient }) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  expect(assistant.tool_resources?.file_search).not.toBeDefined(); // ensure the assistant has no files

  await loadChatPage(page);

  // Select assistant
  await expect(page.getByTestId('assistants-select-btn')).not.toBeDisabled();
  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  const messages = page.getByTestId('message');
  await sendMessage(page, newMessage1);
  await waitForResponseToComplete(page);
  await expect(messages).toHaveCount(2);

  // Cleanup
  await deleteActiveThread(page, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

// Note - these error cases do not test all edge cases. ex. completed response comes back empty, /chat/assistants
// partially completes then fails, stream fails, etc...
test('displays an error toast if /chat/assistants throws while getting a response from an assistant', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadChatPage(page);

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await page.route('*/**/chat/assistants', async (route) => {
    await route.abort('failed');
  });
  await sendMessage(page, newMessage1);

  await expect(page.getByText(ERROR_GETTING_ASSISTANT_MSG_TOAST().title)).toBeVisible();
  const messages = await page.getByTestId('message').all();
  expect(messages).toHaveLength(0);
});

test('displays an error toast if /chat/assistants returns a 500 when getting a response from an assistant 2', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadChatPage(page);

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await page.route('*/**/chat/assistants', async (route) => {
    await route.fulfill({ status: 500 });
  });
  await sendMessage(page, newMessage1);

  await expect(page.getByText(ERROR_GETTING_ASSISTANT_MSG_TOAST().title)).toBeVisible();
  const messages = await page.getByTestId('message').all();
  expect(messages).toHaveLength(1);
});

test('displays an error toast if /chat/assistants returns a 200 with no body when getting a response from an assistant 3', async ({
  page,
  openAIClient
}) => {
  const assistant = await createAssistantWithApi({ openAIClient });
  await loadChatPage(page);

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant!.name!).click();

  await page.route('*/**/chat/assistants', async (route) => {
    await route.fulfill({ status: 200 });
  });
  await sendMessage(page, newMessage1);

  await expect(page.getByText(ERROR_GETTING_ASSISTANT_MSG_TOAST().title)).toBeVisible();
  const messages = await page.getByTestId('message').all();
  expect(messages).toHaveLength(0);
});
