import { expect, test } from './fixtures';
import { loadApiKeyPage, loadChatPage } from './helpers';

test('it can navigate to the API key page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByLabel('Settings').click();
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
  await page.getByRole('button', { name: 'Close' }).click({ force: true });
  await expect(page.getByText('Save secret key')).not.toBeVisible();

});

