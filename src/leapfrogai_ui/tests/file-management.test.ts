import { expect, test } from './fixtures';
import { loadChatPage } from './helpers';

test('it can navigate to the file management page', async ({ page }) => {
  await loadChatPage(page);

  await page.getByLabel('Settings').click();
  await page.getByText('File Management').click();

  await expect(page).toHaveTitle('LeapfrogAI - File Management');
});
