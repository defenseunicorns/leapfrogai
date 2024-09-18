import { expect, test } from './fixtures';
import { loadChatPage } from './helpers/navigationHelpers';
import { createPDF, deleteFixtureFile, uploadFiles } from './helpers/fileHelpers';
import { deleteActiveThread } from './helpers/threadHelpers';
import { faker } from '@faker-js/faker';

test('it can translate an audio file', async ({ page, openAIClient }) => {
  await loadChatPage(page);

  await uploadFiles({
    page,
    filenames: ['spanish.m4a'],
    testId: 'upload-file-btn'
  });

  const chatTools = page.getByTestId('chat-tools');
  await chatTools.getByRole('button', { name: 'Translate spanish.m4a' }).click();

  await expect(page.getByText(`Translating spanish.m4a`)).toBeVisible();
  await expect(page.getByTestId('message')).toHaveCount(2);
  const messages = await page.getByTestId('message').all();
  const responseText = await messages[1].innerText();
  expect(responseText).toContain('cat');

  await deleteActiveThread(page, openAIClient);
});

test('it can transcribe an audio file', async ({ page, openAIClient }) => {
  await loadChatPage(page);

  await uploadFiles({
    page,
    filenames: ['spanish.m4a'],
    testId: 'upload-file-btn'
  });

  const chatTools = page.getByTestId('chat-tools');
  await chatTools.getByRole('button', { name: 'Transcribe spanish.m4a' }).click();

  await expect(page.getByText(`Transcribing spanish.m4a`)).toBeVisible();
  await expect(page.getByTestId('message')).toHaveCount(2);
  const messages = await page.getByTestId('message').all();
  const responseText = await messages[1].innerText();
  expect(responseText).toContain('gato');

  await deleteActiveThread(page, openAIClient);
});

test('it can removes the audio file but keeps other files after translating', async ({
  page,
  openAIClient
}) => {
  await loadChatPage(page);
  const fakeContent = faker.word.words(3);
  const pdfFilename = await createPDF({ content: fakeContent, filename: 'shortname.pdf' });

  await uploadFiles({
    page,
    filenames: ['spanish.m4a', pdfFilename],
    testId: 'upload-file-btn'
  });

  await page.getByTestId('spanish.m4a-uploaded');
  await page.getByTestId(`${pdfFilename}-uploaded`);

  const messagesContainer = page.getByTestId('messages-container');
  const chatToolsContainer = page.getByTestId('chat-tools');

  const chatToolsPDFFileCard = chatToolsContainer.getByTestId(`${pdfFilename}-file-uploaded-card`);
  const chatToolsAudioCard = chatToolsContainer.getByTestId('spanish.m4a-file-uploaded-card');

  await expect(chatToolsPDFFileCard).toBeVisible();
  await expect(chatToolsAudioCard).toBeVisible();

  const translateBtn = chatToolsContainer.getByRole('button', { name: 'Translate spanish.m4a' });
  await translateBtn.click();

  await expect(page.getByTestId('message')).toHaveCount(2);

  await expect(chatToolsAudioCard).not.toBeVisible();
  await expect(translateBtn).not.toBeVisible();

  await expect(messagesContainer.getByTestId('spanish.m4a-file-uploaded-card')).toBeVisible();
  await expect(chatToolsPDFFileCard).toBeVisible();

  // cleanup
  deleteFixtureFile(pdfFilename);
  await deleteActiveThread(page, openAIClient);
});

test("it can summarize a file's content", async ({ page, openAIClient }) => {
  await loadChatPage(page);
  const fakeContent = faker.word.words(3);
  const pdfFilename = await createPDF({ content: fakeContent, filename: 'shortname.pdf' });

  await uploadFiles({
    page,
    filenames: ['spanish.m4a', pdfFilename],
    testId: 'upload-file-btn'
  });

  const messagesContainer = page.getByTestId('messages-container');
  const chatToolsContainer = page.getByTestId('chat-tools');

  const summarizeBtn = chatToolsContainer.getByRole('button', { name: `Summarize ${pdfFilename}` });
  await summarizeBtn.click();

  await expect(messagesContainer.getByText(`Summarize ${pdfFilename}`)).toBeVisible();
  await expect(page.getByTestId('message')).toHaveCount(2);

  // cleanup
  deleteFixtureFile(pdfFilename);
  await deleteActiveThread(page, openAIClient);
});
