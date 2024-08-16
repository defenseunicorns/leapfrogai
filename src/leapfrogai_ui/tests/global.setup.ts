import { test as setup } from './fixtures';
import * as OTPAuth from 'otpauth';
import { delay } from 'msw';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/'); // go to the home page
  await delay(2000); // allow page to fully hydrate
  if (process.env.PUBLIC_DISABLE_KEYCLOAK === 'true') {
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
  } else {
    // With Keycloak
    const emailField = page.getByLabel('Username or email');
    const passwordField = page.getByLabel('Password');
    await page.getByRole('button', { name: 'Log In' }).click();
    await emailField.fill(process.env.USERNAME!);
    console.log('password is: ', process.env.PASSWORD!)
    await passwordField.click();
    await passwordField.fill(process.env.PASSWORD!);

    await page.getByRole('button', { name: 'Log In' }).click();

    if (process.env.TEST_ENV !== 'CI') {
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
    }
  }

  // Wait until the page receives the cookies.
  //
  // Login flow sets cookies in the process of several redirects.
  // Wait for the final URL to ensure that the cookies are actually set.
  await page.waitForURL('/chat');

  // Alternatively, you can wait until the page reaches a state where all cookies are set.
  //   await expect(page.getByRole('button', { name: 'View profile and more' })).toBeVisible();

  // End of authentication steps.

  await page.context().storageState({ path: authFile });
});
