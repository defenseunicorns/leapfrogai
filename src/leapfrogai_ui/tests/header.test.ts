import { expect, test } from './fixtures';

// Note - testing that the sidenav is hidden when on small screens and not expanded by the menu button was deemed not possible with
// playwright because Carbon doesn't actually hide it in a way that playwright can detect, https://playwright.dev/docs/actionability#visible
// Carbon uses transform: translateX(-16rem) to move it off the screen, but Playwright still sees it

test('it only shows the hamburger menu on small screens', async ({ page }) => {
  // Unable to apply test id to just the hamburger menu because the element is not exposed by carbon components svelte
  // Instead, we test that an addional button is added to the banner when the screen is small
  // If more buttons are added to the banner, this test will need to be updated
  await page.setViewportSize({ width: 600, height: 600 });
  await page.goto('/chat');
  await expect(page.getByRole('banner').getByRole('button')).toHaveCount(3);

  await page.setViewportSize({ width: 1800, height: 800 });
  await expect(page.getByRole('banner').getByRole('button')).toHaveCount(2);
});
