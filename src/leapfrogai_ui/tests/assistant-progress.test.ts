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

// Note - fully testing the assistant progress toast has proven difficult with Playwright. Sometimes the websocket
// connection for the Supabase realtime listeners works, and sometimes it does not. Here we test that the
// toast exists with the files, but nothing further.
test('when creating an assistant with files, an assistant progress toast is displayed', async ({
  page,
  openAIClient
}) => {
  const assistantInput = getFakeAssistantInput();
  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF({ filename: filename1 });
  await createPDF({ filename: filename2 });
  const uploadedFile1 = await uploadFileWithApi(filename1, 'application/pdf', openAIClient);
  const uploadedFile2 = await uploadFileWithApi(filename2, 'application/pdf', openAIClient);

  await loadNewAssistantPage(page);

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('tagline').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.getByTestId('file-select-dropdown-btn').click();
  const fileSelectContainer = page.getByTestId('file-select-container');
  await fileSelectContainer.getByTestId(`${uploadedFile1.id}-checkbox`).check();
  await fileSelectContainer.getByTestId(`${uploadedFile2.id}-checkbox`).check();

  await page.getByRole('button', { name: 'Save' }).click();
  await page.waitForURL('/chat/assistants-management');

  await expect(page.getByTestId(`file-${uploadedFile1.id}-vector-in-progress`)).toBeVisible();
  await expect(page.getByTestId(`file-${uploadedFile2.id}-vector-pending`)).toBeVisible();

  // cleanup
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
  await deleteAssistantCard(assistantInput.name, page);
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
});
