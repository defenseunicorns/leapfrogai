import { expect, test } from './fixtures';
import {
  createAssistantWithApi,
  deleteAssistant,
  deleteAssistantWithApi
} from './helpers';
import { getFakeAssistantInput } from '$testUtils/fakeData';
import { delay } from 'msw';
import {deleteFileWithApi, deleteTestFilesWithApi, uploadFile, uploadFileWithApi} from "./helpers/fileHelpers";

test('can edit an assistant and attach files to it', async ({ page, openAIClient }) => {
  const uploadedFile1 = await uploadFileWithApi('test.pdf', openAIClient);
  const uploadedFile2 = await uploadFileWithApi('test2.pdf', openAIClient);
  const assistant = await createAssistantWithApi(openAIClient);
  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  await page.getByRole('button', { name: 'Open menu' }).click();
  await page.getByLabel('Choose an item').locator('label').nth(1).click();
  await page.getByLabel('Choose an item').locator('label').nth(2).click();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

test('can create a new assistant and attach files to it', async ({ page, openAIClient }) => {
  const assistantInput = getFakeAssistantInput();
  const uploadedFile1 = await uploadFileWithApi('test.pdf', openAIClient);
  const uploadedFile2 = await uploadFileWithApi('test2.pdf', openAIClient);
  await page.goto(`/chat/assistants-management/new`);

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.getByRole('button', { name: 'Open menu' }).click();
  await page.getByLabel('Choose an item').locator('label').nth(1).click();
  await page.getByLabel('Choose an item').locator('label').nth(2).click();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Created')).toBeVisible();

  // Cleanup
  await deleteAssistant(page, assistantInput.name);
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
});

test('it can edit an assistant and remove a file', async ({ page, openAIClient }) => {
  const uploadedFile1 = await uploadFileWithApi('test.pdf', openAIClient);
  const uploadedFile2 = await uploadFileWithApi('test2.pdf', openAIClient);
  const assistant = await createAssistantWithApi(openAIClient);
  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  // Create assistant with files
  await page.getByRole('button', { name: 'Open menu' }).click();
  await page.getByLabel('Choose an item').locator('label').nth(1).click();
  await page.getByLabel('Choose an item').locator('label').nth(2).click();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  await page.getByTestId(`assistant-tile-${assistant.name}`).getByTestId('overflow-menu').click();
  await page.getByRole('menuitem', { name: 'Edit' }).click();
  await page.waitForURL('/chat/assistants-management/edit/**/*');

  // Deselect
  await page.locator('.bx--file-close').first().click();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
  await deleteAssistantWithApi(assistant.id, openAIClient);
});

test('while creating an assistant, it can upload new files and save the assistant', async ({
  page,
  openAIClient
}) => {
  const assistantInput = getFakeAssistantInput();
  const fileName = 'test.pdf';

  await page.goto('/chat/assistants-management/new');

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, fileName, 'Upload new data source');

  const saveBtn = await page.getByRole('button', { name: 'Save' });
  expect(saveBtn).toBeDisabled();
  await expect(saveBtn).not.toBeDisabled();

  await saveBtn.click();
  await expect(page.getByText(`${fileName} uploaded successfully.`)).toBeVisible();
  await expect(page.getByText('Assistant Created')).toBeVisible();

  // Cleanup
  await deleteAssistant(page, assistantInput.name);
  await deleteTestFilesWithApi(openAIClient);
});

test('while editing an assistant, it can upload new files and save the assistant', async ({
  page,
  openAIClient
}) => {
  const fileName = 'test.pdf';
  const assistant = await createAssistantWithApi(openAIClient);
  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, fileName, 'Upload new data source');

  const saveBtn = await page.getByRole('button', { name: 'Save' });
  expect(saveBtn).toBeDisabled();
  await expect(saveBtn).not.toBeDisabled();

  await saveBtn.click();
  await expect(page.getByText(`${fileName} uploaded successfully.`)).toBeVisible();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
  await deleteTestFilesWithApi(openAIClient);
});

test('it displays a failed toast and temporarily failed uploader item when a the file upload endpoint completely fails', async ({
  page
}) => {
  const fileName = 'test.pdf';
  // Mock a complete backend failure
  await page.route('*/**/chat/file-management', async (route) => {
    await route.abort('failed');
  });

  await page.goto('/chat/assistants-management/new');

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, fileName, 'Upload new data source');

  await expect(page.getByText(`Upload failed`)).toBeVisible();
  await expect(page.getByTestId(`${fileName}-error-uploader-item`)).toBeVisible();
  await delay(1500);
  await expect(page.getByTestId(`${fileName}-error-uploader-item`)).not.toBeVisible();
});

test('it displays an uploading indicator temporarily when uploading a file', async ({ page }) => {
  const fileName = 'test.pdf';
  await page.goto('/chat/assistants-management/new');

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, fileName, 'Upload new data source');

  await expect(page.getByTestId(`${fileName}-uploading-uploader-item`)).toBeVisible();
  await expect(page.getByTestId(`${fileName}-uploading-uploader-item`)).not.toBeVisible();
});
