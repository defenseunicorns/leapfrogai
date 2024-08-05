import { expect, test } from './fixtures';

test('it can log out', async ({ page }) => {
  await page.goto('/chat');
  await expect(page).toHaveTitle('LeapfrogAI - Chat');
  await page.getByTestId('header-user-btn').click();
  await page.getByTestId('user-drawer').getByLabel('Log Out').click();

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
