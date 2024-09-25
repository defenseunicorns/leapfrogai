import { expect, test } from './fixtures';
import { getSimpleMathQuestion } from './helpers/helpers';
import {
  createPDF,
  createTextFile,
  createWordFile,
  deleteFixtureFile,
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
import { getFakeAssistantInput } from '../testUtils/fakeData';
import { createAssistantWithApi } from './helpers/assistantHelpers';
import { MAX_NUM_FILES_UPLOAD_MSG_TOAST } from '../src/lib/constants/toastMessages';
import {
  APPROX_MAX_CHARACTERS,
  FILE_UPLOAD_PROMPT,
  MAX_NUM_FILES_UPLOAD
} from '../src/lib/constants';
import {
  ERROR_UPLOADING_FILE_MSG,
  FILE_CONTEXT_TOO_LARGE_ERROR_MSG
} from '../src/lib/constants/errors';
import { shortenFileName } from '../src/lib/helpers/stringHelpers';
import { loadChatPage } from './helpers/navigationHelpers';

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
  // confirm remove btn is not present while uploading
  await expect(page.getByTestId(`${wordFilename}-remove-btn`)).not.toBeVisible();

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

  expect(hiddenMessage).toBeDefined();

  expect(hiddenMessage!.content[0].text.value).toContain(shortenFileName(pdfFilename));
  expect(hiddenMessage!.content[0].text.value).toContain(shortenFileName(textFilename));
  expect(hiddenMessage!.content[0].text.value).toContain(shortenFileName(wordFilename));

  expect(hiddenMessage!.content[0].text.value).toContain(fakeContent1);
  expect(hiddenMessage!.content[0].text.value).toContain(fakeContent2);
  expect(hiddenMessage!.content[0].text.value).toContain(fakeContent3);

  // cleanup
  deleteFixtureFile(pdfFilename);
  deleteFixtureFile(textFilename);
  deleteFixtureFile(wordFilename);
  await deleteActiveThread(page, openAIClient);
});

test('it can remove attached files', async ({ page }) => {
  await loadChatPage(page);

  const pdfFilename1 = await createPDF({ filename: 'shortName1.pdf' });
  const pdfFilename2 = await createPDF({ filename: 'shortName2.pdf' });

  await uploadFiles({
    page,
    filenames: [pdfFilename1, pdfFilename2],
    testId: 'upload-file-btn'
  });

  await expect(page.getByTestId(`${pdfFilename1}-uploaded`)).toBeVisible();
  await expect(page.getByTestId(`${pdfFilename2}-uploaded`)).toBeVisible();

  const card = page.getByTestId(`${pdfFilename2}-file-uploaded-card`);
  await card.getByText(pdfFilename2).hover();
  await card.getByTestId(`${pdfFilename2}-remove-btn`).click();

  await expect(page.getByTestId(`${pdfFilename1}-uploaded`)).toBeVisible();
  await expect(page.getByTestId(`${pdfFilename2}-uploaded`)).not.toBeVisible();

  // cleanup
  deleteFixtureFile(pdfFilename1);
  deleteFixtureFile(pdfFilename2);
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

  // cleanup
  deleteFixtureFile(filename);
});

test('it shows an error on the file if there is an error processing a file', async ({ page }) => {
  const filename = createWordFile(); // this file is first converted to pdf which we are mocking to fail

  await loadChatPage(page);

  await page.route('*/**/api/files/parse-text', async (route) => {
    await route.abort('failed');
  });

  await uploadFiles({
    page,
    filenames: [filename],
    testId: 'upload-file-btn'
  });

  await expect(page.getByText(ERROR_UPLOADING_FILE_MSG)).toBeVisible();

  // cleanup
  deleteFixtureFile(filename);
});

test('it adds an error message if a file is too large to add to the context', async ({ page }) => {
  const adjustedMax =
    APPROX_MAX_CHARACTERS -
    Number(process.env.PUBLIC_MESSAGE_LENGTH_LIMIT) -
    FILE_UPLOAD_PROMPT.length -
    2;
  process.env.PUBLIC_MESSAGE_LENGTH_LIMIT = `${APPROX_MAX_CHARACTERS - FILE_UPLOAD_PROMPT.length - 2 + 10}`;
  const filename = createWordFile({
    content: 'a'.repeat(adjustedMax + 1)
  }); // this file is first converted to pdf which we are mocking to fail

  await loadChatPage(page);

  await uploadFiles({
    page,
    filenames: [filename],
    testId: 'upload-file-btn'
  });

  await expect(page.getByText(FILE_CONTEXT_TOO_LARGE_ERROR_MSG)).toBeVisible();

  // cleanup
  deleteFixtureFile(filename);
});

test('it limits the number of files that can be uploaded', async ({ page }) => {
  await loadChatPage(page);

  const filenames: string[] = [];
  for (let i = 0; i < MAX_NUM_FILES_UPLOAD + 1; i++) {
    const filename = await createPDF();
    filenames.push(filename);
  }

  await uploadFiles({
    page,
    filenames,
    testId: 'upload-file-btn'
  });

  await expect(page.getByText(MAX_NUM_FILES_UPLOAD_MSG_TOAST().subtitle!)).toBeVisible();

  // Cleanup
  for (const filename of filenames) {
    deleteFixtureFile(filename);
  }
});
