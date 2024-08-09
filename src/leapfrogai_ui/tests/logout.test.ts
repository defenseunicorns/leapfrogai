import { expect, test } from './fixtures';

test('it can log out', async ({ page }) => {
  await page.goto('/chat');
  await expect(page).toHaveTitle('LeapfrogAI - Chat');
  await page.getByTestId('header-profile-btn').click();
  await page
    .getByTestId('profile-dropdown')
    .getByRole('button', { name: /log out/i })
    .click();

  await page.waitForURL('/');

  if (process.env.PUBLIC_DISABLE_KEYCLOAK === 'true') {
    await expect(page.getByText('Sign In')).toBeVisible();
  } else {
    const loginBtn = page.getByRole('button', { name: /Log In with UDS SSO/i });
    await expect(loginBtn).toBeVisible();
    await loginBtn.click();
    await page.waitForURL(`**/*/realms/uds/**/*`); // ensure full logout of keycloak (not just supabase)
  }
});
