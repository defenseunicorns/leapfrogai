import { expect, test } from './fixtures';
import { createAssistantWithApi, deleteAssistant, deleteAssistantWithApi } from './helpers/helpers';
import { getFakeAssistantInput } from '$testUtils/fakeData';
import { delay } from 'msw';
import {
  createPDF,
  deleteAllGeneratedFixtureFiles,
  deleteAllTestFilesWithApi,
  deleteFileByName,
  deleteFileWithApi,
  deleteFixtureFile,
  deleteTestFilesWithApi,
  uploadFile,
  uploadFileWithApi
} from './helpers/fileHelpers';
import { faker } from '@faker-js/faker';

test.afterAll(() => {
  deleteAllGeneratedFixtureFiles(); // cleanup any files that were not deleted during tests (e.g. due to test failure)
});

test.afterAll(async ({ openAIClient }) => {
  await deleteAllTestFilesWithApi(openAIClient);
});

test('can edit an assistant and attach files to it', async ({ page, openAIClient }) => {
  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename1);
  await createPDF(filename2);

  const uploadedFile1 = await uploadFileWithApi(filename1, openAIClient);
  const uploadedFile2 = await uploadFileWithApi(filename2, openAIClient);
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
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
});

test('can create a new assistant and attach files to it', async ({ page, openAIClient }) => {
  const assistantInput = getFakeAssistantInput();
  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename1);
  await createPDF(filename2);
  const uploadedFile1 = await uploadFileWithApi(filename1, openAIClient);
  const uploadedFile2 = await uploadFileWithApi(filename2, openAIClient);
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
  expect(page.waitForURL('/chat/assistants-management'));
  await deleteAssistant(page, assistantInput.name);
  await deleteFileWithApi(uploadedFile1.id, openAIClient);
  await deleteFileWithApi(uploadedFile2.id, openAIClient);
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
});

test('it can edit an assistant and remove a file', async ({ page, openAIClient }) => {
  const filename1 = `${faker.word.noun()}-test.pdf`;
  const filename2 = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename1);
  await createPDF(filename2);
  const uploadedFile1 = await uploadFileWithApi(filename1, openAIClient);
  const uploadedFile2 = await uploadFileWithApi(filename2, openAIClient);
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
  deleteFixtureFile(filename1);
  deleteFixtureFile(filename2);
});

test('while creating an assistant, it can upload new files and save the assistant', async ({
  page,
  openAIClient
}) => {
  const assistantInput = getFakeAssistantInput();
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  await page.goto('/chat/assistants-management/new');

  await page.getByLabel('name').fill(assistantInput.name);
  await page.getByLabel('description').fill(assistantInput.description);
  await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, filename, 'Upload new data source');

  const saveBtn = await page.getByRole('button', { name: 'Save' });
  expect(saveBtn).toBeDisabled();
  await expect(saveBtn).not.toBeDisabled();

  await saveBtn.click();
  await expect(page.getByText(`${filename} imported successfully.`)).toBeVisible();
  await expect(page.getByText('Assistant Created')).toBeVisible();

  // Cleanup
  expect(page.waitForURL('/chat/assistants-management'));
  await deleteAssistant(page, assistantInput.name);
  await deleteTestFilesWithApi(openAIClient);
  deleteFixtureFile(filename);
  await deleteFileByName(filename, openAIClient);
});

test('while editing an assistant, it can upload new files and save the assistant', async ({
  page,
  openAIClient
}) => {
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  const assistant = await createAssistantWithApi(openAIClient);
  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, filename, 'Upload new data source');

  const saveBtn = await page.getByRole('button', { name: 'Save' });
  expect(saveBtn).toBeDisabled();
  await expect(saveBtn).not.toBeDisabled();

  await saveBtn.click();
  await expect(page.getByText(`${filename} imported successfully.`)).toBeVisible();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteAssistantWithApi(assistant.id, openAIClient);
  await deleteTestFilesWithApi(openAIClient);
  await deleteFileByName(filename, openAIClient);
  deleteFixtureFile(filename);
});

test('it displays a failed toast and temporarily failed uploader item when a the file upload endpoint completely fails', async ({
  page,
  openAIClient
}) => {
  // Mock a complete backend failure
  await page.route('*/**/chat/file-management', async (route) => {
    await route.abort('failed');
  });

  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  await page.goto('/chat/assistants-management/new');

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, filename, 'Upload new data source');

  await expect(page.getByText(`Upload Failed`)).toBeVisible();
  await expect(page.getByTestId(`${filename}-error-uploader-item`)).toBeVisible();
  await delay(1500);
  await expect(page.getByTestId(`${filename}-error-uploader-item`)).not.toBeVisible();

  // Cleanup
  deleteFixtureFile(filename);
  await deleteFileByName(filename, openAIClient);
});

test('it displays an uploading indicator temporarily when uploading a file', async ({
  page,
  openAIClient
}) => {
  const filename = `${faker.word.noun()}-test.pdf`;
  await createPDF(filename);

  await page.goto('/chat/assistants-management/new');

  await page.getByRole('button', { name: 'Open menu' }).click();
  await uploadFile(page, filename, 'Upload new data source');

  await expect(page.getByTestId(`${filename}-uploading-uploader-item`)).toBeVisible();
  await expect(page.getByTestId(`${filename}-uploading-uploader-item`)).not.toBeVisible();

  // Cleanup
  deleteFixtureFile(filename);
  await deleteFileByName(filename, openAIClient);
});
