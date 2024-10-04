import { expect, test } from './fixtures';
import { getFakeAssistantInput } from '$testUtils/fakeData';
import { deleteAssistantCard } from './helpers/assistantHelpers';
import { faker } from '@faker-js/faker';
import {
  createPDF,
  deleteFileWithApi,
  deleteFixtureFile,
  uploadFileWithApi
} from './helpers/fileHelpers';
import { loadNewAssistantPage } from './helpers/navigationHelpers';
import type { FileObject } from 'openai/resources/files';

// Note - fully testing the assistant progress toast has proven difficult with Playwright. Sometimes the websocket
// connection for the Supabase realtime listeners works, and sometimes it does not. Here we test that the
// toast exists with the files, but nothing further.
test('when creating an assistant with files, an assistant progress toast is displayed', async ({
  page,
  openAIClient
}) => {
  const assistantInput = getFakeAssistantInput();
  const numFiles = 2;
  const filenames: string[] = [];
  const uploadedFiles: FileObject[] = [];

  for (let i = 0; i < numFiles; i++) {
    const filename = `${faker.word.noun()}-test.pdf`;
    filenames.push(filename);
    await createPDF({ filename });
    const uploadedFile = await uploadFileWithApi(filename, 'application/pdf', openAIClient);
    uploadedFiles.push(uploadedFile);
  }

  await loadNewAssistantPage(page);

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('tagline').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.getByTestId('file-select-dropdown-btn').click();
  const fileSelectContainer = page.getByTestId('file-select-container');
  for (const file of uploadedFiles) {
    await fileSelectContainer.getByTestId(`${file.id}-checkbox`).check();
  }

  await page.getByRole('button', { name: 'Save' }).click();

  const inProgressSelector = `file-${uploadedFiles[0].id}-vector-in-progress`;
  const completedSelector = `file-${uploadedFiles[0].id}-vector-completed`;

  // Second file is pending
  await expect(page.getByTestId(`file-${uploadedFiles[1].id}-vector-pending`)).toBeVisible();

  // Check for either "in-progress" or "completed" state for the first file, it can happen really fast so this prevents
  // a flaky test
  const progressToast = await page.waitForSelector(
    `[data-testid="${inProgressSelector}"], [data-testid="${completedSelector}"]`,
    {
      timeout: 30000
    }
  );
  expect(progressToast).toBeTruthy();

  await page.waitForURL('/chat/assistants-management');

  // cleanup
  for (const filename of filenames) {
    deleteFixtureFile(filename);
  }
  for (const file of uploadedFiles) {
    await deleteFileWithApi(file.id, openAIClient);
  }
  await deleteAssistantCard(assistantInput.name, page);
});
