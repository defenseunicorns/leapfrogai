import { expect, test } from './fixtures';

test('it only shows the open/close sidebar button on small screens', async ({ page }) => {
  await page.setViewportSize({ width: 600, height: 600 });
  await page.goto('/chat');
  await expect(page.getByTestId('open-sidebar-btn')).toBeVisible();

  await page.setViewportSize({ width: 1800, height: 800 });
  await expect(page.getByTestId('open-sidebar-btn')).not.toBeVisible();
  await expect(page.getByTestId('close-sidebar-btn')).not.toBeVisible();
});

test('it opens the sidebar when the open/close sidebar button is clicked', async ({ page }) => {
  await page.setViewportSize({ width: 600, height: 600 });
  await page.goto('/chat');

  await page.getByTestId('open-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).toBeVisible();
  await page.getByTestId('close-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).not.toBeVisible();
  await page.getByTestId('open-sidebar-btn').click();
  await expect(page.getByTestId('sidebar')).toBeVisible();
});
