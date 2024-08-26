import { expect, test } from './fixtures';
import { getSimpleMathQuestion, loadChatPage } from './helpers/helpers';
import {
  createPDF,
  createTextFile,
  createWordFile,
  uploadFiles,
  uploadFileWithApi
} from './helpers/fileHelpers';
import {
  deleteActiveThread,
  getLastUrlParam,
  sendMessage,
  waitForResponseToComplete
} from './helpers/threadHelpers';
import { faker } from '@faker-js/faker';
import { getFakeAssistantInput } from '$testUtils/fakeData';
import { createAssistantWithApi } from './helpers/assistantHelpers';
import { ERROR_PROCESSING_FILE_MSG_TOAST } from '$constants/toastMessages';
import type { ActionResult } from '@sveltejs/kit';

test('it attaches multiple files of different types and creates a hidden message with their content', async ({
  page,
  openAIClient
}) => {
  await loadChatPage(page);

  // Note - if you use too many words, they get cutoff in the fake PDF
  const fakeContent1 = faker.word.words(3);
  const fakeContent2 = faker.word.words(3);
  const fakeContent3 = faker.word.words(3);

  const pdfFilename = await createPDF({ content: fakeContent1 });
  const textFilename = createTextFile({ content: fakeContent2 });
  const wordFilename = createWordFile({ content: fakeContent3 });

  await uploadFiles({
    page,
    filenames: [pdfFilename, textFilename, wordFilename],
    testId: 'upload-file-btn'
  });

  await page.getByTestId(`${pdfFilename}-uploading`);
  await page.getByTestId(`${textFilename}-uploading`);
  await page.getByTestId(`${wordFilename}-uploading`);

  await expect(page.getByTestId(`${pdfFilename}-uploading`)).not.toBeVisible({ timeout: 20000 });
  await expect(page.getByTestId(`${textFilename}-uploading`)).not.toBeVisible({ timeout: 20000 });
  await expect(page.getByTestId(`${wordFilename}-uploading`)).not.toBeVisible({ timeout: 20000 });

  await page.getByTestId(`${pdfFilename}-uploaded`);
  await page.getByTestId(`${textFilename}-uploaded`);
  await page.getByTestId(`${wordFilename}-uploaded`);

  const messages = page.getByTestId('message');
  await expect(messages).toHaveCount(0);
  await sendMessage(page, getSimpleMathQuestion());
  await waitForResponseToComplete(page);

  // The created message with our file context is hidden, so we fetch it and
  // ensure it was created with the right content
  const threadId = getLastUrlParam(page);
  const messagesPage = await openAIClient.beta.threads.messages.list(threadId);

  const hiddenMessage = messagesPage.data.find(
    (message) => message.metadata?.hideMessage === 'true'
  );
  console.log('hiddenMessage', hiddenMessage?.content);

  expect(hiddenMessage).toBeDefined();

  expect(hiddenMessage!.content[0].text.value).toContain(pdfFilename);
  expect(hiddenMessage!.content[0].text.value).toContain(textFilename);
  expect(hiddenMessage!.content[0].text.value).toContain(wordFilename);

  expect(hiddenMessage!.content[0].text.value).toContain(fakeContent1);
  expect(hiddenMessage!.content[0].text.value).toContain(fakeContent2);
  expect(hiddenMessage!.content[0].text.value).toContain(fakeContent3);

  // cleanup
  await deleteActiveThread(page, openAIClient);
});

test('it can remove attached files', async ({ page }) => {
  await loadChatPage(page);

  const pdfFilename1 = await createPDF();
  const pdfFilename2 = await createPDF();

  await uploadFiles({
    page,
    filenames: [pdfFilename1, pdfFilename2],
    testId: 'upload-file-btn'
  });

  await page.getByTestId(`${pdfFilename1}-uploaded`);
  await page.getByTestId(`${pdfFilename2}-uploaded`);

  await page.getByText(pdfFilename2).hover();
  await page.getByTestId(`${pdfFilename2}-remove-btn`).click();

  await expect(page.getByTestId(`${pdfFilename1}-uploaded`)).toBeVisible();
  await expect(page.getByTestId(`${pdfFilename2}-uploaded`)).not.toBeVisible();
});
test('it removes the file btn and attached files when switching to an assistant', async ({
  page,
  openAIClient
}) => {
  const filename = await createPDF();
  const uploadedFile = await uploadFileWithApi(filename, 'application/pdf', openAIClient);
  const fakeAssistantInput = getFakeAssistantInput([uploadedFile.id]);
  const assistant = await createAssistantWithApi({
    assistantInput: fakeAssistantInput,
    openAIClient
  });

  await loadChatPage(page);

  await expect(page.getByTestId('upload-file-btn')).toBeVisible();

  const assistantDropdown = page.getByTestId('assistants-select-btn');
  await assistantDropdown.click();
  await page.getByText(assistant.name!).click();

  await expect(page.getByTestId('upload-file-bnt')).not.toBeVisible();
});

test('it displays a toast and removes files when there is an error processing the pdf', async ({
  page
}) => {
  const filename = createWordFile(); // this file is first converted to pdf which we are mocking to fail

  await loadChatPage(page);

  await page.route('*/**/chat', async (route) => {
    if (route.request().method() === 'POST') {
      const result: ActionResult = {
        type: 'failure',
        status: 500
      };

      await route.fulfill({ json: result });
    } else {
      const response = await route.fetch();
      await route.fulfill({ response });
    }
  });

  await uploadFiles({
    page,
    filenames: [filename],
    testId: 'upload-file-btn'
  });

  await expect(page.getByText(ERROR_PROCESSING_FILE_MSG_TOAST().title)).toBeVisible();
});
