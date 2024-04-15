import { expect, test } from '@playwright/test';

test('it can log out', async ({ page }) => {
	await page.goto('/chat');
	await expect(page).toHaveTitle('LeapfrogAI - Chat');
	await page.getByLabel('User').click();
	await page.getByLabel('Log Out').click();

	await page.waitForURL('http://localhost:4173');

	await expect(page.getByText('Log In')).toBeVisible();
});
