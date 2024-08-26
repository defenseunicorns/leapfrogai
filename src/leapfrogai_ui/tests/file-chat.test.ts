import { expect, test } from './fixtures';
import { getSimpleMathQuestion, loadChatPage } from './helpers/helpers';
import { createPDF, createTextFile, createWordFile, uploadFile } from './helpers/fileHelpers';
import { getLastUrlParam, sendMessage } from './helpers/threadHelpers';
import { faker } from '@faker-js/faker';

test('it attaches multiple files and creates a hidden message with their content', async ({
  page,
  openAIClient
}) => {
  await loadChatPage(page);

  const fakeContent1 = faker.word.words(10);
  const fakeContent2 = faker.word.words(10);
  const fakeContent3 = faker.word.words(10);

  const pdfFilename = await createPDF({ content: fakeContent1 });
  const textFilename = createTextFile({ content: fakeContent2 });
  const wordFilename = createWordFile({ content: fakeContent3 });

  await uploadFile(page, [pdfFilename, textFilename, wordFilename], 'upload-file-btn', true);

  await page.getByTestId(`${pdfFilename}-uploading`);
  await page.getByTestId(`${textFilename}-uploading`);
  await page.getByTestId(`${wordFilename}-uploading`);

  await expect(page.getByTestId(`${pdfFilename}-uploading`)).not.toBeVisible();
  await expect(page.getByTestId(`${textFilename}-uploading`)).not.toBeVisible();
  await expect(page.getByTestId(`${wordFilename}-uploading`)).not.toBeVisible();

  await page.getByTestId(`${pdfFilename}-uploaded`);
  await page.getByTestId(`${textFilename}-uploaded`);
  await page.getByTestId(`${wordFilename}-uploaded`);

  await sendMessage(page, getSimpleMathQuestion());

  const threadId = getLastUrlParam(page);
  const messagesPage = await openAIClient.beta.threads.messages.list(threadId);

  expect(messagesPage.data[1].metadata!.hideMessage).toEqual(true);

  expect(messagesPage.data[1].content).toContain(pdfFilename);
  expect(messagesPage.data[1].content).toContain(textFilename);
  expect(messagesPage.data[1].content).toContain(wordFilename);

  expect(messagesPage.data[1].content).toContain(fakeContent1);
  expect(messagesPage.data[1].content).toContain(fakeContent2);
  expect(messagesPage.data[1].content).toContain(fakeContent3);
});
// test('it removes the file btn and attached files when switching to an assistant', async ({
//   page
// }) => {});
