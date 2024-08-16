import { expect, test as setup } from './fixtures';
import * as OTPAuth from 'otpauth';
import { delay } from 'msw';
import type { Page } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

const doSupabaseLogin = async (page: Page) => {
  await page.goto('/'); // go to the home page
  await delay(2000); // allow page to fully hydrate
  // when running in Github CI, create a new account because we don't have seed migrations
  const emailField = page.getByTestId('email-input');
  const passwordField = page.getByTestId('password-input');
  if (process.env.TEST_ENV === 'CI') {
    await emailField.click();
    await emailField.fill('ci_user@test.com');
    await passwordField.click();
    await passwordField.fill('password123');

    const emailText = await emailField.innerText();
    const passwordText = await passwordField.innerText();
    if (emailText !== 'ci_user@test.com') await emailField.fill('ci_user@test.com');
    if (passwordText !== 'password123') await passwordField.fill('password123');

    await page.getByTestId('submit-btn').click();
  } else {
    // uses local supabase test users, logs in directly with Supabase, no Keycloak
    await page.getByTestId('toggle-submit-btn').click();
    await emailField.click();
    await emailField.fill('user1@test.com');
    await passwordField.click();
    await passwordField.fill('password123');
    await page.getByTestId('submit-btn').click();
  }
};

const login = async (page: Page) => {
  if (process.env.PUBLIC_DISABLE_KEYCLOAK === 'true') {
    await doSupabaseLogin(page);
  } else {
    await doKeycloakLogin(page);
  }
};

const logout = async (page: Page) => {
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
};

const doKeycloakLogin = async (page: Page) => {
  await page.goto('/'); // go to the home page
  await delay(2000); // allow page to fully hydrate
  // With Keycloak
  await page.getByRole('button', { name: 'Log In' }).click();
  await page.getByLabel('Username or email').fill(process.env.USERNAME!);
  await page.getByLabel('Password').click();
  await page.getByLabel('Password').fill(process.env.PASSWORD!);
  await page.getByRole('button', { name: 'Log In' }).click();

  const totp = new OTPAuth.TOTP({
    issuer: 'Unicorn Delivery Service',
    algorithm: 'SHA1',
    digits: 6,
    period: 30,
    secret: process.env.MFA_SECRET!
  });
  const code = totp.generate();
  await page.getByLabel('Six digit code').fill(code);
  await page.getByRole('button', { name: 'Log In' }).click();
};

setup('authenticate', async ({ page }) => {
  page.on('pageerror', (err) => {
    console.log(err.message);
  });

  await login(page);

  // Wait until the page receives the cookies.
  //
  // Login flow sets cookies in the process of several redirects.
  // Wait for the final URL to ensure that the cookies are actually set.
  await page.waitForURL('/chat');

  // First test log out, then log back in and continue. We don't want to put logout in its own test, because it
  // will invalidate the session and cause other tests to fail
  await logout(page);

  // Log back in to begin rest of tests
  await login(page);

  // Alternatively, you can wait until the page reaches a state where all cookies are set.
  //   await expect(page.getByRole('button', { name: 'View profile and more' })).toBeVisible();

  // End of authentication steps.

  await page.context().storageState({ path: authFile });
});
