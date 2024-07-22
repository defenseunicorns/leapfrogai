import { expect, test } from './fixtures';
import { getTableRow, loadApiKeyPage, loadChatPage } from './helpers/helpers';

test('it can navigate to the API key page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByTestId('header-settings-btn').click();
  await page.getByText('API Keys').click();

  await expect(page).toHaveTitle('LeapfrogAI - API Keys');
});

test('it can create and delete an API key', async ({ page }) => {
  await loadApiKeyPage(page);
  const keyName = 'new test key';
  await page.getByRole('button', { name: 'Create new', exact: true }).click();
  await page.getByLabel('name').fill(keyName);
  await page.getByText('60 Days').click();
  await page.getByRole('button', { name: 'Create', exact: true }).click();
  await expect(page.getByText(`${keyName} created successfully`)).toBeVisible();
  await page.getByRole('button', { name: 'Close', exact: true }).click({ force: true });
  await expect(page.getByText('Save secret key')).not.toBeVisible();
  const row = await getTableRow(page, keyName);
  expect(row).not.toBeNull();
  await row!.getByRole('checkbox').check({ force: true });
  const deleteBtn = page.getByRole('button', { name: 'delete' });
  await deleteBtn.click();
  await expect(page.getByText(`Are you sure you want to delete ${keyName}?`)).toBeVisible();
  const deleteBtns = await page.getByRole('button', { name: 'delete' }).all();
  await deleteBtns[1].click();
  await expect(page.getByText('Key Deleted')).toBeVisible();
});
