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

  await expect(page.getByTestId('loading-msg')).toHaveCount(1); // loading skeleton
  await expect(page.getByTestId('loading-msg')).not.toBeVisible({ timeout: 30000 });
  await expect(page.getByTestId('message')).toHaveCount(2);
  // Edit and regen disabled for translated messages
  await expect(page.getByTestId('edit-message')).not.toBeVisible();
  await expect(page.getByTestId('regenerate btn')).not.toBeVisible();
  const messages = await page.getByTestId('message').all();
  const responseText = await messages[1].innerText();
  expect(responseText).toContain('unicorn');

  //cleanup
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

  await expect(page.getByTestId('loading-msg')).toHaveCount(1); // loading skeleton
  await expect(page.getByTestId('loading-msg')).not.toBeVisible({ timeout: 30000 });
  await expect(page.getByTestId('message')).toHaveCount(2);
  // Edit and regen disabled for translated messages
  await expect(page.getByTestId('edit-message')).not.toBeVisible();
  await expect(page.getByTestId('regenerate btn')).not.toBeVisible();
  const messages = await page.getByTestId('message').all();
  const responseText = await messages[1].innerText();
  expect(responseText).toContain('unicorn');

  //cleanup
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

test('has buttons to scroll when there are lots of files for both the list of uploaded files and file actions', async ({
  page
}) => {
  const fakeContent = faker.word.words(3);
  const fileNames: string[] = [];
  for (let i = 0; i < 10; i++) {
    const fileName = await createPDF({
      content: fakeContent,
      filename: `${faker.word.noun()}.pdf`
    });
    fileNames.push(fileName);
  }

  await loadChatPage(page);

  const fileActionsCarousel = page.getByTestId('file-actions-carousel');
  const uploadedFilesCarousel = page.getByTestId('uploaded-files-carousel');

  await expect(fileActionsCarousel.getByText('Previous')).not.toBeVisible();
  await expect(fileActionsCarousel.getByText('Next')).not.toBeVisible();
  await expect(uploadedFilesCarousel.getByText('Previous')).not.toBeVisible();
  await expect(uploadedFilesCarousel.getByText('Next')).not.toBeVisible();

  await uploadFiles({
    page,
    filenames: fileNames,
    testId: 'upload-file-btn'
  });
  await expect(fileActionsCarousel.getByText('Next')).toBeVisible();
  await fileActionsCarousel.getByText('Next').click();
  await expect(fileActionsCarousel.getByText('Previous')).toBeVisible();

  await expect(uploadedFilesCarousel.getByText('Next')).toBeVisible();
  await uploadedFilesCarousel.getByText('Next').click();
  await expect(uploadedFilesCarousel.getByText('Previous')).toBeVisible();

  //cleanup
  for (const filename of fileNames) {
    deleteFixtureFile(filename);
  }
});
