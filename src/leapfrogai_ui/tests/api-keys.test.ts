import { expect, test } from './fixtures';
import { getTableRow } from './helpers/helpers';
import { loadApiKeyPage, loadChatPage } from './helpers/navigationHelpers';

test('it can navigate to the API key page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByTestId('header-settings-btn').click();
  await page.getByText('API Keys').click();

  await expect(page).toHaveTitle('LeapfrogAI - API Keys');
});

test('it can create and delete an API key', async ({ page }) => {
  await loadApiKeyPage(page);
  const keyName = 'new test key';
  await page.getByLabel('create new').click();
  const createModal = page.getByTestId('create-api-key-modal');
  await createModal.getByRole('textbox').fill(keyName);
  await page.getByText('60 Days').click();
  await page.getByRole('button', { name: 'Create', exact: true }).click();
  await expect(page.getByText(`${keyName} created successfully`)).toBeVisible();
  await page.getByRole('button', { name: 'Close', exact: true }).click({ force: true });
  await expect(page.getByText('Save secret key')).not.toBeVisible();

  const row = await getTableRow(page, keyName, 'api-keys-table');
  await row.getByRole('checkbox').check();
  const deleteBtn = page.getByRole('button', { name: 'delete' });
  await deleteBtn.click();
  const deleteModal = page.getByTestId('delete-api-key-modal');
  await expect(deleteModal.getByText(`Are you sure you want to delete`)).toBeVisible();
  const confirmDeleteBtn = deleteModal.getByRole('button', { name: 'delete' });
  await confirmDeleteBtn.click();
  await expect(page.getByText('Key Deleted')).toBeVisible();
});
