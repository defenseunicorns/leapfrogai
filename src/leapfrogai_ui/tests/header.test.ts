import { expect, test } from '@playwright/test';

// Note - testing that the sidenav is hidden when on small screens and not expanded by the menu button was deemed not possible with
// playwright because Carbon doesn't actually hide it in a way that playwright can detect, https://playwright.dev/docs/actionability#visible
// Carbon uses transform: translateX(-16rem) to move it off the screen, but Playwright still sees it

test('it only shows the hamburger menu on small screens', async ({ page }) => {
	await page.setViewportSize({ width: 600, height: 600 });
	await page.goto('/chat');
	await expect(page.getByRole('banner').getByRole('button')).toHaveCount(2);

	await page.setViewportSize({ width: 1800, height: 800 });
	await expect(page.getByRole('banner').getByRole('button')).toHaveCount(1);
});
