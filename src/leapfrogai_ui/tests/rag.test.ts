import { expect, test } from './fixtures';
import {
  createAssistantWithApi,
  deleteAssistantWithApi,
  deleteFileWithApi,
  uploadFileWithApi
} from './helpers';
import { getFakeAssistantInput } from '$testUtils/fakeData';

test('can edit an assistant and attach files to it', async ({ page }) => {
  const uploadedFile1 = await uploadFileWithApi('test.pdf');
  const uploadedFile2 = await uploadFileWithApi('test2.pdf');
  const assistant = await createAssistantWithApi();
  await page.goto(`/chat/assistants-management/edit/${assistant.id}`);

  await page.getByRole('button', { name: 'Open menu' }).click();
  await page.getByLabel('Choose an item').locator('label').nth(1).click();
  await page.getByLabel('Choose an item').locator('label').nth(2).click();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Assistant Updated')).toBeVisible();

  // Cleanup
  await deleteFileWithApi(uploadedFile1.id);
  await deleteFileWithApi(uploadedFile2.id);
  await deleteAssistantWithApi(assistant.id);
});

test('can create a new assistant and attach files to it', async ({ page }) => {
  const assistantInput = getFakeAssistantInput();
  const uploadedFile1 = await uploadFileWithApi('test.pdf');
  const uploadedFile2 = await uploadFileWithApi('test2.pdf');
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
  await page
    .getByTestId(`assistant-tile-${assistantInput.name}`)
    .getByTestId('overflow-menu')
    .click();
  // click overflow menu delete btn
  await page.getByRole('menuitem', { name: 'Delete' }).click();
  // click modal actual delete btn
  await page.getByRole('button', { name: 'Delete' }).click();

  await deleteFileWithApi(uploadedFile1.id);
  await deleteFileWithApi(uploadedFile2.id);
});

test('it can edit an assistant and remove a file', async ({ page }) => {
  const uploadedFile1 = await uploadFileWithApi('test.pdf');
  const uploadedFile2 = await uploadFileWithApi('test2.pdf');
  const assistant = await createAssistantWithApi();
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
  await deleteFileWithApi(uploadedFile1.id);
  await deleteFileWithApi(uploadedFile2.id);
  await deleteAssistantWithApi(assistant.id);
});
