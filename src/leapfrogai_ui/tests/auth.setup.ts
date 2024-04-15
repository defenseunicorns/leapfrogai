import { test as setup } from '@playwright/test';
const authFile = 'playwright/.auth/user.json';
import * as OTPAuth from 'otpauth';

setup('authenticate', async ({ page }) => {
	// Perform authentication steps. Replace these actions with your own.
	await page.goto('http://localhost:4173');
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

	// Chrome gets stuck here for an unknown reason, does not happen in real life
	// This hack allows the test to continue
	// ref: https://github.com/microsoft/playwright/issues/16160
	// I suspect it is an issue with the Supbase callback, but the output in the Playwright UI does not show the error page
	// I was able to see the error when using a VSCode Playwright plugin that records your actions
	await page.waitForLoadState('domcontentloaded');
	await page.reload();

	// Wait until the page receives the cookies.
	//
	// Login flow sets cookies in the process of several redirects.
	// Wait for the final URL to ensure that the cookies are actually set.
	await page.waitForURL('http://localhost:4173/chat');

	// Alternatively, you can wait until the page reaches a state where all cookies are set.
	//   await expect(page.getByRole('button', { name: 'View profile and more' })).toBeVisible();

	// End of authentication steps.

	await page.context().storageState({ path: authFile });
});
