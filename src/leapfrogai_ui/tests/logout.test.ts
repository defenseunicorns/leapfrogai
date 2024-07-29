import { expect, test } from './fixtures';

test('it can log out', async ({ page }) => {
  await page.goto('/chat');
  await expect(page).toHaveTitle('LeapfrogAI - Chat');
  await page.getByLabel('User').click();
  await page.getByLabel('Log Out').click();

  await page.waitForURL('/');

  if (process.env.PUBLIC_DISABLE_KEYCLOAK === 'true') {
    await expect(page.getByText('Sign In')).toBeVisible();
  } else {
    const loginBtn = page.getByText('Log In');
    await expect(loginBtn).toBeVisible();
    await loginBtn.click();
    await expect(page.getByText('Log In with UDS SSO')).toBeVisible();
  }
});
